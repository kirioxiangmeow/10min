from django import forms
from django.core.exceptions import ValidationError

def words_validator(comment):
    if len(comment) < 4:
        raise ValidationError('喂，字数不够啊喂！')

def comment_validator(comment):
    taboo =['清真','蛤蛤','江泽民','续一秒','长者','习习蛤蛤','螂臂挡车','中央大学','跑得快','华莱士','大新闻','谈笑风生']
    if any(i in comment for i in taboo) :
            raise ValidationError('喂，不许乱说话！')


class CommentForm(forms.Form):
    name = forms.CharField(max_length=50)
    comment = forms.CharField(
        widget=forms.Textarea(),
        error_messages={
            'required': '咦，你不填东西我怎么提交？'
            },
        validators=[words_validator, comment_validator],
        )
