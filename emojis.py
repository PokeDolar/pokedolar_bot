from random import sample


def sad_emoji():
    emojis = '😕😟🙁☹️😮😲🥺😦😧😨😰😥😢😭😱😖😣😞😓😩😫😤😡😠🤬💩😾😿🙀'
    return sample(emojis, 1)[0]

def happy_emoji():
    emojis = '😀😃😄😁😆😅🙂🙃😉😍😛🤑🤡😶'
    return sample(emojis, 1)[0]