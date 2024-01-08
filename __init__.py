from os.path import join, dirname

from json_database import JsonStorage

from ovos_utils.ocp import MediaType, PlaybackType
from ovos_workshop.decorators.ocp import ocp_search
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill


class EpicHorrorTheatreSkill(OVOSCommonPlaybackSkill):
    def __init__(self, *args, **kwargs):
        self.db = JsonStorage(join(dirname(__file__),
                                   "res", "epichorrortheatre.json"))
        self.supported_media = [MediaType.RADIO_THEATRE,
                                MediaType.AUDIOBOOK]
        self.default_bg = join(dirname(__file__), "ui", "bg.jpg")
        self.skill_icon = join(dirname(__file__), "ui", "icon.png")
        super().__init__(*args, **kwargs)

        self.register_ocp_keyword(MediaType.AUDIOBOOK,
                                  "book_name", list(self.db.keys()))
        self.register_ocp_keyword(MediaType.AUDIOBOOK,
                                  "book_author", ["Lovecraft", "H. P. Lovecraft"])
        self.register_ocp_keyword(MediaType.RADIO_THEATRE,
                                  "radio_drama_director",
                                  ["Atlanta Radio Theatre"])
        self.register_ocp_keyword(MediaType.RADIO_THEATRE,
                                  "radio_drama_streaming_provider",
                                  ["EpicHorrorTheatre", "Epic Horror Theatre"])

    def clean_vocs(self, phrase):
        phrase = self.remove_voc(phrase, "reading")
        phrase = self.remove_voc(phrase, "lovecraft")
        phrase = self.remove_voc(phrase, "atlanta")
        phrase = self.remove_voc(phrase, "epic_horror")
        phrase = self.remove_voc(phrase, "audio_theatre")
        phrase = self.remove_voc(phrase, "play")
        phrase = phrase.strip()
        return phrase

    def get_base_score(self, phrase, media_type):
        original = phrase
        score = 0

        if self.voc_match(original, "atlanta"):
            score += 15

        if self.voc_match(phrase, "audio_theatre") or \
                media_type == MediaType.RADIO_THEATRE:
            score += 35
        elif media_type == MediaType.AUDIOBOOK:
            score += 15

        if self.voc_match(original, "horror"):
            score += 15
        elif self.voc_match(original, "epic_horror"):
            score += 30

        if self.voc_match(original, "lovecraft"):
            score += 50

        return score

    @ocp_search()
    def ocp_epichorrortheatre_playlist(self, phrase, media_type):
        score = self.get_base_score(phrase, media_type)
        if self.voc_match(phrase, "atlanta"):
            score += 15
        if self.voc_match(phrase, "audio_theatre") or \
                media_type == MediaType.RADIO_THEATRE:
            score += 10
        pl = [
            {
                "match_confidence": score,
                "media_type": MediaType.AUDIOBOOK,
                "uri": entry["uri"],
                "playback": PlaybackType.AUDIO,
                "image": join(dirname(__file__), entry["image"]),
                "bg_image": self.default_bg,
                "skill_icon": self.skill_icon,
                "title": title,
                "author": "H. P. Lovecraft",
                "album": "by Atlanta Radio Theatre"
            } for title, entry in self.db.items()
        ]
        if pl:
            yield {
                "match_confidence": score,
                "media_type": MediaType.AUDIOBOOK,
                "playlist": pl,
                "playback": PlaybackType.AUDIO,
                "skill_icon": self.skill_icon,
                "image": self.default_bg,
                "bg_image": self.default_bg,
                "title": "Epic Horror Theatre (Atlanta Radio Theatre)",
                "author": "H. P. Lovecraft",
                "album": "by Atlanta Radio Theatre"
            }

    @ocp_search()
    def search(self, phrase, media_type):
        score = self.get_base_score(phrase, media_type)
        phrase = self.clean_vocs(phrase)
        scores = {k: score for k, v in self.db.items()}
        if self.voc_match(phrase, "color_out_of_space"):
            scores["The Color Out of Space"] += 70
        elif self.voc_match(phrase, "innsmouth"):
            scores["The Shadow Over Innsmouth"] += 70
        elif self.voc_match(phrase, "mountains_of_madness"):
            scores["At The Mountains of Madness"] += 70
        elif media_type not in [MediaType.RADIO_THEATRE, MediaType.AUDIOBOOK]:
            return

        if score >= 50:
            for k in scores:
                yield {
                    "match_confidence": min(100, scores[k]),
                    "media_type": MediaType.AUDIOBOOK,
                    "uri": self.db[k]["uri"],
                    "playback": PlaybackType.AUDIO,
                    "image": join(dirname(__file__), self.db[k]["image"]),
                    "bg_image": self.default_bg,
                    "skill_icon": self.skill_icon,
                    "title": k,
                    "author": "H. P. Lovecraft",
                    "album": "by Atlanta Radio Theatre"
                }
