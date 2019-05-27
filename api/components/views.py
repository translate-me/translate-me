from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import TextComposite, TextFragment, ImageFragment
from .serializers import TextCompositeSerializer, TextFragmentSerializer, \
                         ImageFragmentSerializer

text_request = {
    'author': 1,
    'context': 'Texto Mockado',
    'content':[
        {
            'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Amet tellus cras adipiscing enim eu turpis egestas. Elementum nibh tellus molestie nunc. Ultrices eros in cursus turpis massa tincidunt dui ut. Cursus turpis massa tincidunt dui. Risus viverra adipiscing at in tellus integer feugiat scelerisque. At ultrices mi tempus imperdiet nulla. Aenean et tortor at risus. Urna neque viverra justo nec ultrices dui sapien eget. Imperdiet dui accumsan sit amet nulla. Felis eget nunc lobortis mattis aliquam faucibus purus in massa. Viverra suspendisse potenti nullam ac tortor vitae purus. Felis imperdiet proin fermentum leo vel orci porta. Fames ac turpis egestas integer eget aliquet nibh praesent. Pulvinar pellentesque habitant morbi tristique senectus et netus et malesuada.',
            'type': 'text'
        },
        {
            'content': 'image1',
            'type': 'image'
        },
        {
            'content': 'image2',
            'type': 'image'
        },
        {
            'content': 'meu querido texto',
            'type': 'text'
        },
        {
            'content': 'minha querida imagem',
            'type': 'image'
        },
        {
            'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Amet tellus cras adipiscing enim eu turpis egestas. Elementum nibh tellus molestie nunc. Ultrices eros in cursus turpis massa tincidunt dui ut. Cursus turpis massa tincidunt dui. Risus viverra adipiscing at in tellus integer feugiat scelerisque. At ultrices mi tempus imperdiet nulla. Aenean et tortor at risus. Urna neque viverra justo nec ultrices dui sapien eget. Imperdiet dui accumsan sit amet nulla. Felis eget nunc lobortis mattis aliquam faucibus purus in massa. Viverra suspendisse potenti nullam ac tortor vitae purus. Felis imperdiet proin fermentum leo vel orci porta. Fames ac turpis egestas integer eget aliquet nibh praesent. Pulvinar pellentesque habitant morbi tristique senectus et netus et malesuada.',
            'type': 'text'
        },
    ]
}

class GetAllFragments(APIView):
    def get(self, request):
        text_composite = TextComposite.objects.get(id=49)
        text_composite.init()

        text_fragments = TextFragment.objects.filter(text=text_composite)
        for i in text_fragments:
            text_composite.add(i)

        image_fragments = ImageFragment.objects.filter(text=text_composite)
        for i in image_fragments:
            text_composite.add(i)

        response = self.get_response(text_composite.get_fragments())
        text_value = {
            'text_value': text_composite.get_value()
        }
        response.insert(0, text_value)

        return Response(response)

    def post(self, request):        
        text_composite = TextComposite()
        text_composite.init()
        text_composite.author = text_request['author']
        text_composite.context = text_request['context']
        text_composite.save()

        self.create_fragments(text_request['content'], text_composite)

        text_composite.save_fragments()
        text_composite.total_fragments = len(text_composite.get_fragments())
        text_composite.save()
        
        return Response('Fragmentos criados com sucesso')

    def create_fragments(self, content, text_composite):
        for i in content:
            if i['type'] == 'text':
                text_frag = TextFragment()
                text_frag.text = text_composite
                text_frag.content = i['content']
                text_frag.value = 50
                text_composite.add(text_frag)

            elif i['type'] == 'image':
                image_frag = ImageFragment()
                image_frag.text = text_composite
                image_frag.image = i['content']
                image_frag.value = 25
                text_composite.add(image_frag)
    
    def get_response(self, text_composite):
        fragments = []
        for i in text_composite:
            if i.get_type() == 'text':
                serializer = TextFragmentSerializer(i)
            elif i.get_type() == 'image':
                serializer = ImageFragmentSerializer(i)

            fragments.append(serializer.data)
        
        return fragments
