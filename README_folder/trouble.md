# Trouble

- 카테고리 페이지 로드 시, 매우 긴 시간을 소비하는 product.all() 발견

  ![trouble_1.png](/README_folder/image/trouble_1.png)

  - 다른 뷰와 차이점을 찾던 중, 차이점을 발견함

    ```python
    class CategoryViewSet(viewsets.ModelViewSet):
        ...
        # filter_fields의 products가 페이지 로드 시, 쿼리 생성
        # -> 속도 저하 원인이 될 수 있음
        filter_backends = [DjangoFilterBackend]
        filter_fields = ('name', 'products')
        ...
    ```

    - [DjangoFilterBackend]의 필드를 이용한 filter가 구현되어 있었음

- DjangFilterBackend 및 filter_fields를 주석처리 한 결과

  ![solution_1](/README_folder/image/solution_1.png)

  - 위에서 발견된 알 수 없는 product 쿼리가 제거 됨

- 기본 django filter backend를 이용할 경우 불필요한 쿼리가 생성될 수 있음



# Trouble

- product_list 및 comment_list 페이지 출력 시, 유사한 쿼리문 생성

  ![problem_product](/README_folder/image/problem_product.png)

  ![trouble_2](/README_folder/image/trouble_2.png)

  - CommentSerializer에서 comments 및 reply를 화면에 출력하기 위한 과정
  - 중첩 댓글을 구현하는 과정에서 재귀를 이용하기 때문에 반복적인 쿼리문 생성

  

- **comment_list(product_detail의 comments):** CacheOps를 이용해 문제 해결

  \[Github] [Redis 정리](https://github.com/navill/port_django_shop/blob/master/README_Folder/redis.md) 

  \[Notion] [cacheops를 이용한 redis](https://www.notion.so/afmadadans/ORM-07b20f43a16d4a448229625e7ad0e920)

  ```python
  class ProductDetailSerializer(serializers.ModelSerializer):
      comments = serializers.SerializerMethodField()
      ...
      
      @cached_as(Product, timeout=120)
      def get_comments(self, obj):
        result = list()
        queryset = Comment.objects.filter(product_id=obj.id, parent=None)
        for obj in queryset:
        serializer = CommentSerializer(obj, context=self.context)
          result.append(serializer.data)
        return result
  ```
  
  - 재귀가 발생하는 시점의 함수에 사용되는 모델(Comment)에 caching을 적용하여 product 및 comment page에서 반복적인 쿼리가 일어나지 않도록 함
  
  - serializer에서 재귀적으로 comment 쿼리를 사용하기 때문에 캐시를 이용하지 않을 경우 중첩 댓글을 출력하는 코드의 구조를 변경할 필요가 있음
  
    

- **product_list:** select_related & prefetch_related를 이용한 중복 쿼리 제거

  - 기존 모델은 Category(부모) - Product - Comment(자식) 관계로 구성됨

  - select_related를 이용해 Category를, prefetch_related를 이용해 Comment를 한 번의 쿼리를 이용해 가져옴

    ```python
    class ProductList(ListCreateAPIView):
        serializer_class = ProductSerializer
        filter_backends = [DjangoFilterBackend]
        filter_class = ProductFilter
        permission_classes = (IsAdminUserOrReadOnly,)
    
        def get_queryset(self):
            qs = Product.objects.select_related('category').prefetch_related('comments').all()
            return qs
    ```

    ![solution_2](/README_folder/image/solution_2.png)

