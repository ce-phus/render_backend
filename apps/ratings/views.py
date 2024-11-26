from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.profiles.models import Profile

from .models import Rating

User = get_user_model()

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_agent_review(request, profile_id):
    try:
        agent_profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    profile_user = User.objects.get(pkid=agent_profile.user.pkid)

    if profile_user.email == request.user.email:
        return Response(
            {"message": "Sorry, You cannot rate yourself"},
            status=status.HTTP_403_FORBIDDEN,
        )

    alreadyExists = agent_profile.agent_review.filter(
        rater=request.user
    ).exists()

    if alreadyExists:
        return Response(
            {"detail": "You have already reviewed this agent"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if data.get("rating", 0) == 0:
        return Response(
            {"detail": "Please select a valid rating"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    review = Rating.objects.create(
        rater=request.user,
        agent=agent_profile,
        rating=data["rating"],
        comment=data.get("comment", ""),
    )

    reviews = agent_profile.agent_review.all()
    agent_profile.num_reviews = reviews.count()
    agent_profile.rating = round(
        sum(review.rating for review in reviews) / reviews.count(), 2
    )
    agent_profile.save()

    return Response({"message": "Review added successfully"}, status=status.HTTP_201_CREATED)
