import logging
from json import JSONDecodeError

from flask import Blueprint, render_template, request

from functions import add_post
from loader.utils import save_picture

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates_name')


@loader_blueprint.route('/post')
def post_page():
    return render_template('main/templates_name/post_list.html')


@loader_blueprint.route('/post', methods=['POST'])
def add_post_page():
    picture = request.files.get('picture')
    content = request.form.get('content')

    if not picture or not content:
        return 'Нет картинки или текста'

    if picture.filename.split('.')[-1] not in ['jpeg', 'png']:
        logging.info('Загруженный файл не картинка')
        return 'Этот формат не поддерживается'
    try:
        picture_path: str = '/' + save_picture(picture)
    except FileNotFoundError:
        logging.error('Фото не найдено')
        return 'Фото не найдено'
    except JSONDecodeError:
        return 'Невалидный файл'
    post: dict = add_post({'pic': picture_path, 'content': content})

    return render_template('loader/templates_name/post_uploaded.html', post=post)
