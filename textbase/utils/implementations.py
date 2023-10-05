import click
from typing import List

def prompt_if(opt_name, opt_value):

    class PromptIf(click.Option):
        def __init__(self, *args, **kwargs):
            kwargs['prompt'] = kwargs.get('prompt', True)
            super(PromptIf, self).__init__(*args, **kwargs)

        def handle_parse_result(self, ctx, opts, args):
            assert any(param.name == opt_name for param in ctx.command.params), \
                f"Param '{opt_name}' not found for option '{self.name}'"

            if opt_name not in ctx.params:
                raise click.UsageError(
                    f"Illegal usage: {opt_name} is a required parameter")

            # remove prompt
            if opt_value not in ctx.params[opt_name]:
                self.prompt = None

            return super(PromptIf, self).handle_parse_result(ctx, opts, args)

    return PromptIf

class ConvertStrToList(click.Option):

    def check_bot_type(self, bot_type):

        VALID_BOT_TYPES = ['textbase', 'meta']
        ERROR_MESSAGE = lambda bot_type: click.style(f"'{bot_type}' is not one of {VALID_BOT_TYPES}", fg='red')

        if isinstance(bot_type, List):
            for bot in bot_type:
                if bot not in VALID_BOT_TYPES:
                    raise click.BadParameter(ERROR_MESSAGE(bot))
        else:
            if bot_type not in VALID_BOT_TYPES:
                raise click.BadParameter(ERROR_MESSAGE(bot_type))

    def type_cast_value(self, ctx, value) -> List:
        try:
            if "," in value:
                list_of_items = value.replace(" ", "").split(",")
                self.check_bot_type(list_of_items)
                return list_of_items
            else:
                self.check_bot_type(value)
                return value
        except click.BadParameter as e:
            raise click.BadParameter(e.message)
