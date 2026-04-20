import random
from typing import List, Literal, Optional

# 상위 빈도 성씨 (통계청 상위권 + 자주 쓰는 성씨)
COMMON_SURNAMES = [
    "김","이","박","최","정","강","조","윤","장","임",
    "오","한","신","서","권","황","안","송","류","홍",
    "전","고","문","양","손","배","백","허","노","하",
    "곽","성","차","주","우","구","민","유","진","지",
    "엄","채","원","천","방","공","현","변"
]

# 복성(두 글자 성) — 필요 시만 포함
RARE_COMPOUND_SURNAMES = ["남궁","제갈","선우","서문","독고","황보","사공","동방","공손","탁"]

# 성별/중성 이름 음절(자주 쓰이는 한글 음절; 한자음 의미는 생략)
# 가중치는 뒤쪽 섹션에서 부여
SYL_MASC = ["민","준","현","우","준","호","도","윤","진","혁","태","성","재","석","훈","기","범","환","건","원"]
SYL_FEM  = ["서","지","수","은","연","아","예","유","린","슬","솔","하","소","채","미","영","희","진","나","현"]
SYL_NEUT = ["은","윤","진","지","현","유","민","연","하","수","성","태","아","예","우","채","서","소","원","도"]

# 간단한 가중치(출현 빈도 느낌만 반영; 합리적/임의 값)
def _weights_for(syllables: List[str]) -> List[int]:
    base = {  # 자주 쓰이는 음절은 가중치↑
        "민":9,"준":10,"현":10,"서":10,"지":10,"수":9,"윤":9,"진":8,"아":8,"예":8,
        "우":8,"채":7,"연":7,"은":8,"하":8,"성":6,"태":7,"영":6,"희":5,"유":7,
        "소":6,"슬":4,"솔":3,"도":4,"재":6,"석":4,"훈":5,"기":5,"범":3,"환":4,"건":4,"원":5,"나":5,"린":6
    }
    return [base.get(s, 3) for s in syllables]  # 기본 3

# 성씨도 아주 대략적인 가중치(김/이/박/최/정 비중↑)
def _surname_weights(surnames: List[str]) -> List[int]:
    boost = {"김":20,"이":18,"박":13,"최":8,"정":7}
    return [boost.get(s, 3) for s in surnames]

def _pick_surname(include_compound: bool) -> str:
    pool = COMMON_SURNAMES[:]
    if include_compound:
        pool = pool + RARE_COMPOUND_SURNAMES
    weights = _surname_weights(pool)
    return random.choices(pool, weights=weights, k=1)[0]

def _pick_syllable(gender: Literal["male","female","any"], position: Literal["first","second"]) -> str:
    # position은 '이름'의 1·2번째 음절 위치. 간단히 같은 풀에서 뽑되 성별로 가중치 달리.
    if gender == "male":
        pool = SYL_MASC + SYL_NEUT
    elif gender == "female":
        pool = SYL_FEM + SYL_NEUT
    else:
        pool = SYL_NEUT + SYL_MASC + SYL_FEM
    weights = _weights_for(pool)
    return random.choices(pool, weights=weights, k=1)[0]

def make_korean_name(
    gender: Literal["male","female","any"]="any",
    include_compound_surname: bool=False,
    two_syllable_given: bool=True,
    separator: str="",            # "" (공백 없음) 또는 " " (성/이름 사이 공백)
) -> str:
    """
    한국식 이름 생성기 (기본: 성 1글자 + 이름 2글자 = 3글자, 공백 없음)
    """
    surname = _pick_surname(include_compound_surname)
    if two_syllable_given:
        given = _pick_syllable(gender, "first") + _pick_syllable(gender, "second")
    else:
        # 드물지만 1음절 이름 옵션
        given = _pick_syllable(gender, "first")
    if separator:
        return f"{surname}{separator}{given}"
    return f"{surname}{given}"


def generate_names(
    n: int,
    gender: Literal["male","female","any"]="any",
    include_compound_surname: bool=False,
    two_syllable_given: bool=True,
    separator: str="",
    unique: bool=False,
    seed: Optional[int]=None,
) -> List[str]:
    """
    n개의 이름을 생성.
    - unique=True: 중복 제거(필요 시 더 뽑아 채움 — 충돌이 많으면 시간이 늘 수 있음)
    - seed: 난수 고정
    """
    if seed is not None:
        random.seed(seed)

    pool = COMMON_SURNAMES[:]
    if include_compound_surname:
        pool = pool + RARE_COMPOUND_SURNAMES
    s_weights = _surname_weights(pool)

    if gender == "male":
        syl_pool = SYL_MASC + SYL_NEUT
    elif gender == "female":
        syl_pool = SYL_FEM + SYL_NEUT
    else:
        syl_pool = SYL_NEUT + SYL_MASC + SYL_FEM
    syl_weights = _weights_for(syl_pool)

    surnames   = random.choices(pool,     weights=s_weights,   k=n)
    first_syls = random.choices(syl_pool, weights=syl_weights, k=n)

    if two_syllable_given:
        second_syls = random.choices(syl_pool, weights=syl_weights, k=n)
        names = [f"{s}{separator}{f}{g}" for s, f, g in zip(surnames, first_syls, second_syls)]
    else:
        names = [f"{s}{separator}{f}" for s, f in zip(surnames, first_syls)]

    if not unique:
        return names

    seen = set()
    result: List[str] = []
    for name in names:
        if name not in seen:
            seen.add(name)
            result.append(name)
    if len(result) < n:
        print(f"[warn] 충돌이 많아 {n}개 중 {len(result)}개만 생성했습니다. 음절 풀을 늘리거나 unique=False를 사용하세요.")
    return result

# 데모
if __name__ == "__main__":
    print("아무 성별 5개:", generate_names(5, gender="any", seed=42))
    print("남성 스타일 5개:", generate_names(5, gender="male", seed=43))
    print("여성 스타일 5개(복성 허용, 공백 포함):", generate_names(5, gender="female", include_compound_surname=True, separator=" ", seed=44))
    print("유일 20개:", generate_names(20, unique=True, seed=45))
