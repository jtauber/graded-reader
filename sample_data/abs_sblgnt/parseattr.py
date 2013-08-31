def person(attr):
    return dict(First="1", Second="2", Third="3", blank="-")[attr.get("Person", "blank")]


def tvm(attr):
    tense = dict(Present="P", Aorist="A", Future="F", Perfect="R", Imperfect="I", Pluperfect="L", blank="-")[attr.get("Tense", "blank")]
    voice = dict(Active="A", Middle="M", Passive="P", blank="-")[attr.get("Voice", "blank")]
    mood = dict(Indicative="I", Subjunctive="S", Imperative="D", Optative="O", Infinitive="N", Participle="P", blank="-", False="?")[attr.get("Mood", "blank")]
    return tense + voice + mood


def number(attr):
    return dict(Singular="S", Plural="P", blank="-")[attr.get("Number", "blank")]


def pn(attr):
    return "{}{}".format(person(attr), number(attr))


def degree(attr):
    return dict(Comparative="C", Superlative="S", blank="-")[attr.get("Degree", "blank")]


def case(attr):
    return {
        "Nominative": "N",
        "Accusative": "A",
        "Genitive": "G",
        "Dative": "D",
        "Vocative": "V",
        "": "-",
        None: "-"
    }[attr.get("Case")]


def cng(attr):
    gender = dict(Masculine="M", Feminine="F", Neuter="N", blank="-")[attr.get("Gender", "blank")]
    return case(attr) + number(attr) + gender


def ccat(attr):
    return "{}{}{}{}".format(person(attr), tvm(attr), cng(attr), degree(attr))


    analysis = attr["Cat"]
    if attr["Cat"] in ["noun"]:
        analysis = "N- ----{}-".format(cng(attr))
    elif attr["Cat"] in ["det"]:
        analysis = "RA ----{}-".format(cng(attr))
    elif attr["Cat"] in ["adj"]:
        analysis = "A- ----{}{}".format(cng(attr), degree(attr))
    elif attr["Cat"] in ["pron"]:
        if attr.get("Relative") == "True":
            pos = "RR"
        elif attr.get("Demonstrative") == "True":
            pos = "RD"
        elif attr.get("Personal") == "True":
            pos = "RP"
        elif attr.get("Interrogative") == "True":
            pos = "RI"
        else:
            pos = "--"
        analysis = "{}- ----{}-".format(pos, cng(attr))
    elif attr["Cat"] in ["verb"]:
        analysis = "V- {}".format(ccat(attr))
    elif attr["Cat"] in ["prep", "conj", "adv", "ptcl", "intj"]:
        analysis = "{}- --------".format(dict(prep="P", conj="C", adv="D", ptcl="X", intj="I")[attr["Cat"]])
    elif attr["Cat"] == "num":
        analysis = "NU --------"
    else:
        raise Exception, attr["Cat"]
    
