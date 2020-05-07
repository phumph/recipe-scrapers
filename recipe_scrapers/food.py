import json

from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string, get_yields


class Food(AbstractScraper):

    @classmethod
    def host(self):
        return 'food.com'

    def title(self):
        return self.soup.find('h1').get_text()

    def total_time(self):
        return get_minutes(self.soup.find(
            'div',
            {'class': 'recipe-facts__time'})
        )

    def yields(self):
        return get_yields(self.soup.find(
            'div',
            {'class': 'recipe-facts__servings'}
        ).get_text())

    def ingredients(self):
        ingredients = self.soup.findAll(
            'li',
            {"class": "recipe-ingredients__item"}
        )

        return [
            normalize_string(ingredient.get_text())
            for ingredient in ingredients
        ]

    def instructions(self):
        instructions = self.soup.findAll(
            'li',
            {"class": "recipe-directions__step"}
        )

        return '\n'.join([
            instruction.get_text()
            for instruction in instructions
        ])

    def ratings(self):
        return round(float(json.loads(
            str().join(self.soup.find(
                'script',
                {'type': 'application/ld+json'}
            ))
        ).get('aggregateRating').get('ratingValue')), 2)
