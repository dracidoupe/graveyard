"""
Module dedicated to working with DDCZ-ahem-specific way of handling HTML.
Strings are stored with all HTML special character encoded to entities and
has to be decoded on output into presentation layer. This module helps with
both.

For code archeologists, this roughly satisfies requirements of `funkceHTML.php`.
`unsafe_encode_valid_creation_html` on the other hand, handles `funkce.php` requirements

"""

import re

# Attributes refer to whitelisted attributes
# Pair refers to whether tag requires corresponding and well-nested closing tag
#      Defaults to True
WHITELISTED_TAGS = {
    "a": {
        "attributes": ["href", "target"]
    },
    "b": {},
    "i": {},
    "h1": {},
    "h2": {},
    "h3": {},
    "h4": {},
    "h5": {},
    "u": {},
    "s": {},
    "strike": {},
    "sub": {},
    "sup": {},
    "em": {},
    "p": {},
    "q": {},
    "cite": {},
    "strong": {},
    "table": {
        "attributes": ["border"]
    },
    "tr": {
        "attributes": ["colspan", "rowspan"],
        "parent_tags": ["table"],
    },
    "td": {
        "attributes": ["colspan", "rowspan"],
        "parent_tags": ["tr"],
    },
    "th": {
        "attributes": ["colspan", "rowspan"],
        "parent_tags": ["tr"],
    },
    "ul": {
        "attributes": ["type"]
    },
    "ol": {},
    "li": {
        "parent_tags": ["ul", "ol"],
    },
    "img": {
        "pair": False,
        "attributes": ["src", "width", "height"],
    },
    "br": {
        "pair": False
    },
    "hr": {
        "attributes": ["width"],
        "pair": False
    },
}

WHITELISTED_TAGS_LIST = WHITELISTED_TAGS.keys()

LEFT_ENTITY = "&lt;"
RIGHT_ENTITY = "&gt;"

MAX_LOOKAHEAD_FROM_LEFT = max(list(map(len, WHITELISTED_TAGS_LIST))) + len(RIGHT_ENTITY)

MAX_ATTRIBUTE_LENGTH = 100

def unsafe_encode_valid_creation_html(entity_string):
    """
    ###
    DEPRECATED: Doesn't do attributes properly. May be used as an transition
    function when cleaning up source on original site.
    ###

    Takes string with HTML entities and naively turn all whitelisted
    encoded HTML tags into their unencoded version. 

    DOESN'T check for tag parity and doesn't accept any attributes.

    Use only for CreationPages text that went through admin review
    """

    for tag in WHITELISTED_TAGS:
        if WHITELISTED_TAGS[tag].get('attributes', False):
            tag_start_regexp_string = tag
            for attr in WHITELISTED_TAGS[tag]['attributes']:
                tag_start_regexp_string += r'(\ ' + attr + r'=\&quot;\S\&quot;)?'
        else:
            tag_start_regexp_string = tag

        if WHITELISTED_TAGS[tag].get('pair', True):
            entity_string = re.sub(
                LEFT_ENTITY+tag_start_regexp_string+RIGHT_ENTITY,
                '<'+tag+'>',
                entity_string,
                flags=re.I
            )

            entity_string = re.sub(
                LEFT_ENTITY+'/'+tag+RIGHT_ENTITY,
                '</'+tag+'>',
                entity_string,
                flags=re.I
            )

        else:
            entity_string = re.sub(
                LEFT_ENTITY+tag_start_regexp_string+'(\ )?(/)?'+RIGHT_ENTITY,
                '<'+tag+'>',
                entity_string,
                flags=re.I
            )

    return entity_string


def unsafe_encode_any_creation_html(entity_string):
    """
    VERY INSECURE AND SHOULD BE REPLACED AS SOON AS THE ORIGINAL VERSION IS GONE

    Temporary replacement for this function used in original site:

        function replace_tags($text){
            $text=ereg_replace("&quot;", "\"", $text);
            $text=ereg_replace("&lt;", "<", $text);
            $text=ereg_replace("&gt;",">", $text);
            //$text=strip_tags($text,"<UL><LI><OL><B><STRONG><BIG><EM><I><P><BR><TABLE><TR><TD><IMG><CENTER><FONT><TH><CAPTION><HR><A><H1><H2><H3><H4><H5><SUP>");
            $text=ereg_replace("&amp;nbsp;","&nbsp;", $text);
            echo $text;
        }

    This function relied on proper HTML editorial review.
    """

    entity_string = re.sub(
        r"\&quot\;",
        "\"",
        entity_string
    )

    entity_string = re.sub(
        LEFT_ENTITY,
        "<",
        entity_string
    )

    entity_string = re.sub(
        RIGHT_ENTITY,
        ">",
        entity_string
    )

    entity_string = re.sub(
        r"\&amp\;nbsp\;",
        "&nbsp;",
        entity_string
    )

    return entity_string


def encode_valid_html(entity_string):
    """
    Take string with HTML entities encoded and return whitelisted and valid
    HTML pairs decoded back into HTML chars.

    FIXME: In the future future, sanitised text in HTML should be stored
    FIXME: In the short future, we should trust database to store non-maligned
           HTML, hence only replacing whitelisted tags on the output. This should
           be much faster than the state machine below that is kinda needed for all
           the requirements from the old version
    """

    # Most straightforward idea for reimplementation is processing char by char
    # and using stack to find out about the current position in the DOM tree

    tag_stack = []
    # in_tag_braces = False
    encoded_safe_string = ""

    i = 0
    while i < len(entity_string):
        char = entity_string[i]

        # TODO: in_tag_braces recognition will be needed with support for tag
        # attributes, now we can just skip by        
        # if not in_tag_braces:
        if char != "&":
            encoded_safe_string += char
            i += 1
            continue
        else:
            if entity_string[i:i+4] == "&lt;":
                if entity_string[i+4] == "/":
                    # Looks like a closing of the tag. Do we have tag on stack?
                    if len(tag_stack) > 0:
                        if entity_string[i+5:i+5+len(tag_stack[-1])].lower() == tag_stack[-1]:
                            # yup, our tag -- remove, render and move on
                            tag = tag_stack.pop()
                            encoded_safe_string += "</%s>" % tag
                            i += 5 # &lt;/
                            i += len(tag)
                            i += 4 # &gt;
                            continue
                        else:
                            encoded_safe_string += char
                            i += 1
                            continue
                    else:
                        # no stack, hence we are not recognising tags:
                        # append and move on
                        encoded_safe_string += char
                        i += 1
                        continue
                else:
                    # Looks like an opening of the tag. Do lookeahead and try
                    # to decide whether it's valid tag
                    #FIXME: Doesn't support <br/> variants
                    #FIXME: Doesn't support </end of tags>
                    #FIXME: Doesn't support tag attributes
                    tag_candidate_string = entity_string[i+4:i+3+MAX_LOOKAHEAD_FROM_LEFT+3].split('&gt;')[0].lower()
                    additional_skip = 0

                    if tag_candidate_string.endswith('/'):
                        tag_candidate_string = tag_candidate_string.rstrip('/')
                        additional_skip +=1 

                    if tag_candidate_string.endswith(' '):
                        tag_candidate_string = tag_candidate_string.rstrip(' ')
                        additional_skip +=1 
                        
                    if tag_candidate_string in WHITELISTED_TAGS_LIST:
                        # Tag detected: render it and move after the tag
                        encoded_safe_string += "<%s>" % tag_candidate_string

                        i += 4 # &lt;
                        i += len(tag_candidate_string)
                        i += additional_skip # account for potential "<tag />" variants
                        i += 4 # &gt;

                        # If it also is a pair tag, put it on stack
                        if not WHITELISTED_TAGS.get(tag_candidate_string, False):
                            tag_stack.append(tag_candidate_string)

                        continue
                    else:

                        encoded_safe_string += char
                        i += 1
                        continue
                        
            else:
                encoded_safe_string += char
                i += 1
                continue

    return encoded_safe_string