import json
import os
import re
from typing import Dict, Any
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.crud.comment import comment_crud
from app.db.base import Comment


def parse_rating(rating_html: str) -> int:
    if not rating_html:
        return 0

    match = re.search(r'rating="(\d+)"', rating_html)
    if match:
        rating = int(match.group(1))
        return max(0, min(rating, 5))
    return 0


def parse_date(date_str: str) -> datetime:
    if not date_str:
        return datetime.now()

    try:
        return datetime.strptime(date_str, '%d.%m.%Y')
    except ValueError:
        return datetime.now()


def parse_files_from_directory(directory_path: str) -> list:
    products = {}
    comments = []
    product_counter = 1

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                    for item in data:
                        product_name = item.get('name', '').strip()
                        review_data = item.get('t', {})

                        if not product_name:
                            continue

                        if product_name not in products:
                            products[product_name] = product_counter
                            product_counter += 1

                        product_id = products[product_name]

                        comment_text = review_data.get('txt', '').strip()
                        if len(comment_text) > 1024:
                            comment_text = comment_text[:1021] + "..."

                        comment_data = {
                            'comment': comment_text,
                            'rating': parse_rating(review_data.get('rating', '')),
                            'date': parse_date(review_data.get('date', '')),
                            'product_id': product_id,
                        }

                        comments.append(comment_data)

            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f"Ошибка JSON в файле {filename}: {e}")
            except Exception as e:
                raise Exception(f"Ошибка при обработке файла {filename}: {e}")

    return comments


def process_comment(db):
    directory_path = "app/db/mock_data"

    parsed_data = parse_files_from_directory(directory_path)

    for data in parsed_data:
        comment = Comment(
            comment=data['comment'],
            rating=data['rating'],
            date=data['date'],
            product_id=data['product_id']
        )
        comment_crud.create(db, comment=comment.comment, rating=comment.rating, date=comment.date,
                            product_id=comment.product_id)
