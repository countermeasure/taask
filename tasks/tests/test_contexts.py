from django.test import TestCase


class ContextTests(TestCase):

    def new_context_cant_have_same_name_as_existing_context(self):
        pass

    def context_cant_be_renamed_with_an_existing_context_name(self):
        pass

    def context_name_cant_consist_only_of_spaces(self):
        pass
    
    def context_name_cant_have_whitespace_at_beginning_or_end(self):
        pass
