from rest_framework.views import APIView
from django_ratelimit.decorators import ratelimit
from apps.customer_user.customer_user_dal import customer_user_dal





class GetStoryDots(APIView):
    def get(self, request):
# @router.get('/get_story_dots', response=ValidEmailCodeOut)
        """
        获取故事点
        """
        story_dots = customer_user_dal.get_story_dots()
        return {'code': 200, 'message': '获取成功', 'data': story_dots}