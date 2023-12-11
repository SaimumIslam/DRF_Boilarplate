from django.db import models

from ua_parser import user_agent_parser


class TokenQuerySet(models.QuerySet):
    MUTATE_FIELD = "device_info"

    def format_device_info(self, user_agent):
        user_agent_dict = user_agent_parser.Parse(user_agent)
        property_key = ["os", "device", "user_agent"]

        device_info = ""
        for key in property_key:
            device_info += user_agent_dict[key].get("family", "") + ";"
        return device_info

    def get(self, *args, **kwargs):
        if self.MUTATE_FIELD in kwargs:
            kwargs[self.MUTATE_FIELD] = self.format_device_info(kwargs[self.MUTATE_FIELD])
        return super().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        if self.MUTATE_FIELD in kwargs:
            kwargs[self.MUTATE_FIELD] = self.format_device_info(kwargs[self.MUTATE_FIELD])
        return super().filter(*args, **kwargs)

    def create(self, **kwargs):
        if self.MUTATE_FIELD in kwargs:
            kwargs[self.MUTATE_FIELD] = self.format_device_info(kwargs[self.MUTATE_FIELD])
        return super().create(**kwargs)

    def update(self, **kwargs):
        if self.MUTATE_FIELD in kwargs:
            kwargs[self.MUTATE_FIELD] = self.format_device_info(kwargs[self.MUTATE_FIELD])
        return super().update(**kwargs)


