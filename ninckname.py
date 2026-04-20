import random
import math
import string
import numpy as np

_SUFFIX_CHARS = np.frombuffer((string.ascii_lowercase + string.digits).encode(), dtype=np.uint8)  # a-z0-9, 36가지
_PREFIX_SPACE = 30 * 31  # ADJECTIVES × NOUNS

def _suffix_length(n: int, max_length: int) -> int:
    # 생일 역설: P(충돌 < 0.1%) 보장을 위해 36^k > 1000 * n^2 / PREFIX_SPACE 만족하는 최소 k
    needed = max(1, 1000 * n * n / _PREFIX_SPACE)
    k = math.ceil(math.log(needed) / math.log(36))
    # 최소 4자, base가 최소 4자 남도록 상한 제한
    return max(4, min(k, max_length - 5))

def _raw_batch(n: int, style: str, add_number: bool, number_range: tuple,
               max_length: int, suf_len: int) -> np.ndarray:
    adjs  = random.choices(ADJECTIVES, k=n)
    nouns = random.choices(NOUNS,      k=n)

    if style == "underscore":
        bases = [f"{a}_{b}" for a, b in zip(adjs, nouns)]
    elif style == "dash":
        bases = [f"{a}-{b}" for a, b in zip(adjs, nouns)]
    elif style == "camel":
        bases = [a + b.capitalize() for a, b in zip(adjs, nouns)]
    else:
        raise ValueError("style must be one of: underscore, dash, camel")

    if add_number:
        nums = np.random.randint(number_range[0], number_range[1] + 1, n)
        mask = np.random.random(n) < 0.7
        bases = [f"{b}.{num}" if m else b for b, num, m in zip(bases, nums, mask)]

    idx = np.random.randint(0, len(_SUFFIX_CHARS), (n, suf_len))
    suffixes = [''.join(chr(c) for c in _SUFFIX_CHARS[row]) for row in idx]

    trim = max_length - suf_len - 1  # _suffix 포함 max_length 초과 방지
    return np.array([f"{b[:trim]}_{s}" for b, s in zip(bases, suffixes)])

ADJECTIVES = [
    "happy", "sleepy", "brave", "curious", "gentle", "wild", "clever",
    "calm", "shiny", "fuzzy", "lazy", "swift", "lucky", "bold", "silent",
    "tiny", "stormy", "crispy", "cozy", "sunny", "snowy", "blue", "green",
    "golden", "silver", "mystic", "cosmic", "retro", "neon", "pixel"
]

NOUNS = [
    "cat", "dog", "otter", "fox", "panda", "bear", "wolf", "lion", "tiger",
    "owl", "whale", "eagle", "koala", "penguin", "seal", "rabbit", "monkey",
    "sun", "moon", "star", "sky", "forest", "mountain", "river", "ocean",
    "storm", "rain", "cloud", "fire", "shadow", "wind"
]

ITEMS = [
    "sword", "shield", "potion", "armor", "ring", "amulet", "boots",
    "helmet", "gloves", "bow", "arrow", "staff", "wand", "dagger",
    "cloak", "belt", "scroll", "gem", "map", "key"
]

def make_username(
    style: str = "underscore",  # "underscore", "dash", "camel"
    add_number: bool = True,
    number_range: tuple = (0, 9999),
    max_length: int = 30,
    seed: int | None = None
) -> str:
    """
    적당히 자연스러운 인터넷 아이디 생성기
    """
    if seed is not None:
        random.seed(seed)

    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    
    # 결합 스타일
    if style == "underscore":
        name = f"{adj}_{noun}"
    elif style == "dash":
        name = f"{adj}-{noun}"
    elif style == "camel":
        name = adj + noun.capitalize()
    else:
        raise ValueError("style must be one of: underscore, dash, camel")
    
    # 숫자 추가
    if add_number and random.random() < 0.7:  # 70% 확률로 숫자 붙이기
        num = str(random.randint(*number_range))
        name = f"{name}.{num}"
    
    # 길이 제한 (길면 중간 자름)
    if len(name) > max_length:
        name = name[:max_length]
    
    return name

def generate_items(
        numItems: int,
        max_length: int = 32,
        seed: int | None = None
) -> np.ndarray:
    if seed is not None:
        random.seed(seed)

    adjs  = random.choices(ADJECTIVES, k=numItems)
    items = random.choices(ITEMS,      k=numItems)
    return np.array([f"{a}-{b}"[:max_length] for a, b in zip(adjs, items)])

def make_item() -> str:
    '''
    무작위 아이템 이름 생성
    '''
    adjective = random.choice(ADJECTIVES)
    item = random.choice(ITEMS)
    return f"{adjective}-{item}"

def generate_usernames(
    numUsernames: int,
    style: str = "underscore",
    add_number: bool = True,
    number_range: tuple = (0, 9999),
    max_length: int = 15,
    seed: int | None = None
) -> np.ndarray:
    if seed is not None:
        random.seed(seed)

    suf_len = _suffix_length(numUsernames, max_length)
    arr = _raw_batch(numUsernames, style, add_number, number_range, max_length, suf_len)

    # 중복 재생성 루프: 중복이 없을 때까지 해당 항목만 교체
    while True:
        _, first_idx = np.unique(arr, return_index=True)
        dup_mask = np.ones(len(arr), dtype=bool)
        dup_mask[first_idx] = False
        num_dups = int(dup_mask.sum())
        if num_dups == 0:
            break
        arr[dup_mask] = _raw_batch(num_dups, style, add_number, number_range, max_length, suf_len)

    return arr

# ✅ 예시
if __name__ == "__main__":
    for name in generate_usernames(numUsernames = 10):
        print(name)

    print("\n-----\n")
    for item in generate_items(numItems = 10):
        print(item)

