
import collections


def part1():
    # 	In an HTTP request, the Accept-Language header describes the list of
    # 	languages that the requester would like content to be returned in. The header
    # 	takes the form of a comma-separated list of language tags. For example:
        
    # 	Accept-Language: en-US, fr-CA, fr-FR
        
    # 	means that the reader would accept:
        
    # 	1. English as spoken in the United States (most preferred)
    # 	2. French as spoken in Canada
    # 	3. French as spoken in France (least preferred)
        
    # 	We're writing a server that needs to return content in an acceptable language
    # 	for the requester, and we want to make use of this header. Our server doesn't
    # 	support every possible language that might be requested (yet!), but there is a
    # 	set of languages that we do support. 
        
    # 	Write a function that receives two arguments:
    # 	an Accept-Language header value as a string and a set of supported languages,
    # 	and returns the list of language tags that will work for the request. The
    # 	language tags should be returned in descending order of preference (the
    # 	same order as they appeared in the header).
        
    # 	In addition to writing this function, you should use tests to demonstrate that it's
    # 	correct, either via an existing testing system or one you create.
        
    # 	Examples:
        
    # 	parse_accept_language(
    # 	  "en-US, fr-CA, fr-FR",  # the client's Accept-Language header, a string
    # 	  ["fr-FR", "en-US"]      # the server's supported languages, a set of strings
    # 	)
    # 	returns: ["en-US", "fr-FR"]
        
    # 	parse_accept_language("fr-CA, fr-FR", ["en-US", "fr-FR"])
    # 	returns: ["fr-FR"]
        
    # 	parse_accept_language("en-US", ["en-US", "fr-CA"])
    # 	returns: ["en-US"]
    return

def part2():
    # 	Accept-Language headers will often also include a language tag that is not
    # /	region-specific - for example, a tag of "en" means "any variant of English". Extend
    # 	your function to support these language tags by letting them match all specific
    # 	variants of the language.
        
    # 	Examples:
        
    # 	parse_accept_language("en", ["en-US", "fr-CA", "fr-FR"])
    # 	returns: ["en-US"]
        
    # 	parse_accept_language("fr", ["en-US", "fr-CA", "fr-FR"])
    # 	returns: ["fr-CA", "fr-FR"]
        
    # 	parse_accept_language("fr-FR, fr", ["en-US", "fr-CA", "fr-FR"])
    # 	returns: ["fr-FR", "fr-CA"]
    return 

def part3():
    # 	Accept-Language headers will sometimes include a "wildcard" entry, represented
    # 	by an asterisk, which means "all other languages". Extend your function to
    # 	support the wildcard entry.
        
    # 	Examples:
        
    # 	parse_accept_language("en-US, *", ["en-US", "fr-CA", "fr-FR"])
    # 	returns: ["en-US", "fr-CA", "fr-FR"]
        
    # 	parse_accept_language("fr-FR, fr, *", ["en-US", "fr-CA", "fr-FR"])
    # 	returns: ["fr-FR", "fr-CA", "en-US"]
    return 

def parse_accept_language(language_header, supported_languages):

    return parse_accept_language4(language_header, supported_languages)

def parse_accept_language1(language_header, supported_languages):

    supported_languages_set = set(supported_languages)
    compatible_languages = []

    for language in language_header.split(","):
        language = language.strip()

        if language in supported_languages_set:
            compatible_languages.append(language)
    
    return compatible_languages

def parse_accept_language2(language_header, supported_languages):

    supported_languages_set = set(supported_languages)
    grouped_languages = collections.defaultdict(set)

    for lang in supported_languages:
        language, region = lang.split('-')
        grouped_languages[language].add(region)

    compatible_languages = []

    for language in language_header.split(","):
        language = language.strip()

        is_regional = '-' in language
        if not is_regional:
            for region in grouped_languages[language]:
                possible_language = f'{language}-{region}'
                if possible_language not in compatible_languages:
                    compatible_languages.append(possible_language)

        elif language in supported_languages_set:
            compatible_languages.append(language)
    
    return compatible_languages

def parse_accept_language3(language_header, supported_languages):

    supported_languages_set = set(supported_languages)
    grouped_languages = collections.defaultdict(set)

    for lang in supported_languages:
        language, region = lang.split('-')
        grouped_languages[language].add(region)

    compatible_languages = []

    for language in language_header.split(","):
        language = language.strip()

        is_regional = '-' in language
        if not is_regional:
            for region in grouped_languages[language]:
                possible_language = f'{language}-{region}'
                if possible_language not in compatible_languages:
                    compatible_languages.append(possible_language)

        elif language in supported_languages_set:
            compatible_languages.append(language)
        
        if language == "*":
            for L in supported_languages:
                if L not in compatible_languages:
                    compatible_languages.append(L)
    
    return compatible_languages

def parse_accept_language4(language_header, supported_languages):
    # 	Part 4
    # 	Accept-Language headers will sometimes include explicit numeric weights (known as
    # 	q-factors) for their entries, which are used to designate certain language tags
    # 	as specifically undesired. For example:
        
    # 	Accept-Language: fr-FR;q=1, fr;q=0.5, fr-CA;q=0
        
    # 	This means that the reader most prefers French as spoken in France, will take
    # 	any variant of French after that, but specifically wants French as spoken in
    # 	Canada only as a last resort. Extend your function to parse and respect q-factors.
        
    # 	Examples:
        
    # 	parse_accept_language("fr-FR;q=1, fr-CA;q=0, fr;q=0.5", ["fr-FR", "fr-CA", "fr-BG"])
    # 	returns: ["fr-FR", "fr-BG", "fr-CA"]
        
    # 	parse_accept_language("fr-FR;q=1, fr-CA;q=0, *;q=0.5", ["fr-FR", "fr-CA", "fr-BG", "en-US"])
    # 	returns: ["fr-FR", "fr-BG", "en-US", "fr-CA"]
        
    # 	parse_accept_language("fr-FR;q=1, fr-CA;q=0.8, *;q=0.5", ["fr-FR", "fr-CA", "fr-BG", "en-US"])

    # NOTE cant have duplicate entries in accept header

    all_languages = set(supported_languages)
    language_groups = collections.defaultdict(set)
    for l_code in supported_languages:
        l, r = l_code.split("-")
        language_groups[l].add(r)
    
    supported_languages = {}
    # added_languages = set()

    for language_weight in language_header.split(","):
        lang, weight = language_weight.strip().split(";")
        weight = float(weight.split('=')[-1])
        is_regional = '-' in lang

        if lang == "*":
            # the reason why were doing this is so that we dont add a language like fr-CA;q=1 then add it again into our list
            # when *;q=0 comes later
            for l in all_languages:
                if l not in supported_languages:
                    supported_languages[l] = weight
                    
        elif not is_regional:
            # we want to add all the regional languages using this region from the grouping map
            for region in language_groups[lang]:
                lang_code = f'{lang}-{region}'
                if lang_code not in supported_languages:
                    supported_languages[lang_code] = weight
        else:
            # regional language, check if it is in set and add it
            supported_languages[lang] = weight
    
    res_set = [ (val, key) for key, val in supported_languages.items() ]
    sorted_languages = sorted( res_set, key= lambda x: -x[0]  )
    return [ lang for weight, lang in sorted_languages ]


def main():
    # parse_accept_language()
    # assert parse_accept_language("en-US, fr-CA, fr-FR", ["fr-FR", "en-US"]) == ["en-US", "fr-FR"]
    # assert parse_accept_language("fr-CA, fr-FR", ["en-US", "fr-FR"]) == ["fr-FR"]
    # assert parse_accept_language("en-US", ["en-US", "fr-CA"]) == ["en-US"]
    # assert parse_accept_language("en-GB", []) == []
    # assert parse_accept_language("en-GB", ["en-US"]) == []
    # assert parse_accept_language("en-US, fr-CA, fr-FR", ["en-US", "fr-CA", "fr-FR"][::-1]) == ["en-US", "fr-CA", "fr-FR"]
    
    
    # assert parse_accept_language("en", ["en-US", "fr-CA", "fr-FR"]) == ["en-US"]
    # # assert parse_accept_language("fr", ["en-US", "fr-CA", "fr-FR"]) == ["fr-CA", "fr-FR"]    
    # assert parse_accept_language("fr-FR, fr", ["en-US", "fr-CA", "fr-FR"]) == ["fr-FR", "fr-CA"]
    # # assert parse_accept_language("fr, fr-CA, fr-FR", ["fr-FR", "en-US"]) == ["fr-FR"] NOT ALLOWED RN
    # assert parse_accept_language("es, ru", ["en-US", "fr-FR"]) == []
    # assert parse_accept_language("ru", []) == []
    # assert parse_accept_language("en-GB, en", []) == []

    # assert parse_accept_language("en, *", ["en-US", "fr-CA", "fr-FR"]) == ["en-US", "fr-CA", "fr-FR"]
    # # assert parse_accept_language("*, fr", ["en-US", "fr-CA", "fr-FR"]) == ["fr-CA", "fr-FR"]    NOT ALLOWED
    # assert parse_accept_language("fr-FR, *", ["en-US", "fr-CA", "fr-FR"]) == ["fr-FR", "en-US", "fr-CA"]
    # assert parse_accept_language("es, ru, *", ["en-US", "fr-FR"]) == ["en-US", "fr-FR"]
    # assert parse_accept_language("es, en-CA, *", ["en-US", "fr-FR"]) == ["en-US", "fr-FR"]
    # assert parse_accept_language("*", ["en-US"]) == ["en-US"]
    # assert parse_accept_language("*", []) == []

    assert parse_accept_language("fr-FR;q=1, fr-CA;q=0, fr;q=0.5", ["fr-FR", "fr-CA", "fr-BG"]) == ["fr-FR", "fr-BG", "fr-CA"]
    assert parse_accept_language("fr-FR;q=1, fr-CA;q=0, *;q=0.5", ["fr-FR", "fr-CA", "fr-BG", "en-US"]) == ["fr-FR", "fr-BG", "en-US", "fr-CA"]
    assert parse_accept_language("fr-FR;q=1, fr-CA;q=0.8, *;q=0.5", ["fr-FR", "fr-CA", "fr-BG", "en-US"]) == ["fr-FR", "fr-CA", "fr-BG", "en-US"]
    




main()
	
