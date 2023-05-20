# * Prompt
#  * Everyday we look at a lot of URLs, for example in our log files from client request.
#  * We want our data science team to perform analytics and machine learning, but:
#  *    1. we want to preserve the privacy of the user, but without completely obfuscating/hashing the URLs and making them useless,
#  *    2. we simply have a lot of data and we want to reduce our storage/processing costs
#  * In real world, we may solve this with hashing; due to the time constraints of the interview, we use numeronyms instead of compress Strings.
#  *
#  * Example starter code
#  * String compress(String s) {
#  *    // requirement 1, 2, etc
#  *    String compressed_s = fx(s);
#  *    return compressed_s;
#  * }
#  *
#  * Part 1
#  * Given a String, split it into "major parts" separated by special char '/'.
#  * For each major part that's split by '/', we can further split it into "minor parts" separated by '.'.
#  * We assume the given Strings:
#  *    - Only have lower case letters and two separators ('/', '.').
#  *    - Have no empty minor parts (no leading / trailing separators or consecutive separators like "/a", "a/", "./..").
#  *    - Have >= 3 letters in each minor part.
#  *
#  * Example:
#  *    stripe.com/payments/checkout/customer.maria
#  *    s4e.c1m/p6s/c6t/c6r.m3a
#  *
#  * Part 2
#  * In some cases, major parts consists of dozens of minor parts, that can still make the output String large.
#  * For example, imagine compressing a URL such as "section/how.to.write.a.java.program.in.one.day".
#  * After compressing it by following the rules in Part 1, the second major part still has 9 minor parts after compression.
#  *
#  * Task:
#  * Therefore, to further compress the String, we want to only keep m (m > 0) compressed minor parts from Part1 within each major part.
#  * If a major part has more than m minor parts, we keep the first (m-1) minor parts as is, but concatenate the first letter of the m-th minor part and the last letter of the last minor part with the count

def compress(s):
    return f'{s[0]}{len(s)-2}{s[-1]}'

def part1(url:str):
    compressed_url = []
    major_parts = url.split('/')

    for each_part in major_parts:
        
        compressed_parts = []
        minor_parts = each_part.split('.')
        
        for part in minor_parts:
            compressed_parts.append(compress(part))

        compressed_url.append('.'.join(compressed_parts))

    return '/'.join(compressed_url)

def part2(url:str, m):
    compressed_url = []
    major_parts = url.split('/')

    for each_part in major_parts:
        
        compressed_parts = []
        minor_parts = each_part.split('.')
        
        for ind, part in enumerate(minor_parts):
            if len(compressed_parts) < m-1:
                compressed_parts.append(compress(part))
            else:
                leftover_len = sum([ len(p) for p in minor_parts[ind:] ])
                something = f'{part[0]}{leftover_len-2}{minor_parts[-1][-1]}'
                compressed_parts.append(something)
                break

        compressed_url.append('.'.join(compressed_parts))

    return '/'.join(compressed_url)
    


def test1():
    assert part1("stripe.com/payments/checkout/customer.maria") == "s4e.c1m/p6s/c6t/c6r.m3a"
    assert part1("stripe.com/stripe.com.something.everything/nothing") == "s4e.c1m/s4e.c1m.s7g.e8g/n5g"
    assert part1("stripe") == "s4e"
    assert part1("stripe.com") == "s4e.c1m"
    assert part1("stripe/com") == "s4e/c1m"
    
def test2():
    assert part2("stripe.com/payments/checkout/customer.maria", 1) == "s7m/p6s/c6t/c11a"
    assert part2("stripe.com/stripe.com.something.everything/nothing", 2) == "s4e.c1m/s4e.c20g/n5g"
    assert part2("stripe", 1) == "s4e"
    assert part2("stripe.com", 1) == "s7m"
    assert part2("stripe/com", 1) == "s4e/c1m"


test1()
test2()

    