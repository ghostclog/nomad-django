from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Perk
from .serializers import PerkSerializer


class Perks(APIView): #퍽들 전체 보기
    def get(self, request): #얻기
        all_perks = Perk.objects.all() # 모든 퍽 객체 호출
        serializer = PerkSerializer(all_perks, many=True) # 가져온 퍽 객체들을 직렬화 / 추가 파리미터로 many를 true로 줌
        return Response(serializer.data)

    def post(self, request): #추가
        serializer = PerkSerializer(data=request.data) # 요청 데이터를 직렬화하고
        if serializer.is_valid(): # 직렬화 한 데이터가 유효한지 체크
            perk = serializer.save() # 유효하면 저장
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors) # 아니면 유효하지 않는 영역에 대해 에러를 발생


class PerkDetail(APIView): #퍽 상세 보기
    def get_object(self, pk): # 퍽 단일 객체 얻기
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk): # 퍽 정보 얻기
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk): # 퍽 정보 수정
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(
                PerkSerializer(updated_perk).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)