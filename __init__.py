from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel, CPSMatchType
import random
import re
from os.path import join, dirname


class EpicHorrorTheatreSkill(CommonPlaySkill):

    def __init__(self):
        super().__init__("Epic Horror Theatre")
        self.supported_media = [CPSMatchType.GENERIC,
                                CPSMatchType.AUDIOBOOK]

    def initialize(self):
        self.add_event('skill-epic-horror-theatre.jarbasskills.home',
                       self.handle_homescreen)

    def get_intro_message(self):
        self.speak_dialog("intro")
        self.gui.show_image(join(dirname(__file__), "ui", "logo.png"))

    # homescreen
    def handle_homescreen(self, message):
        # TODO selection menu
        media_path = join(dirname(__file__), "media")
        url = join(media_path, random.choice(
            ["At The Mountains of Madness.mp3",
             "The Shadow Over Innsmouth.mp3",
             "The Color Out of Space.mp3"
             ]))
        self.CPS_play(url)

    # common play
    def remove_voc(self, utt, voc_filename, lang=None):
        lang = lang or self.lang
        cache_key = lang + voc_filename

        if cache_key not in self.voc_match_cache:
            self.voc_match(utt, voc_filename, lang)

        if utt:
            # Check for matches against complete words
            for i in self.voc_match_cache[cache_key]:
                # Substitute only whole words matching the token
                utt = re.sub(r'\b' + i + r"\b", "", utt)

        return utt

    def clean_vocs(self, phrase):
        phrase = self.remove_voc(phrase, "reading")
        phrase = self.remove_voc(phrase, "atlanta")
        phrase = self.remove_voc(phrase, "epic_horror")
        phrase = self.remove_voc(phrase, "audio_theatre")
        phrase = self.remove_voc(phrase, "play")
        phrase = phrase.strip()
        return phrase

    def CPS_match_query_phrase(self, phrase, media_type):
        media_path = join(dirname(__file__), "media")
        original = phrase
        match = None

        score = 0

        if media_type == CPSMatchType.AUDIOBOOK:
            score += 0.1
            match = CPSMatchLevel.GENERIC

        if self.voc_match(original, "atlanta"):
            score += 0.15
            match = CPSMatchLevel.CATEGORY

        if self.voc_match(original, "audio_theatre"):
            score += 0.15
            match = CPSMatchLevel.CATEGORY

        if self.voc_match(original, "epic_horror"):
            score += 0.15
            match = CPSMatchLevel.CATEGORY

        phrase = self.clean_vocs(phrase)

        if self.voc_match(phrase, "lovecraft"):
            score += 0.5
            match = CPSMatchLevel.ARTIST

        if self.voc_match(phrase, "color_out_of_space"):
            match = CPSMatchLevel.TITLE
            score += 0.7
            url = join(media_path, "The Color Out of Space.mp3")
        elif self.voc_match(phrase, "innsmouth"):
            match = CPSMatchLevel.TITLE
            score += 0.7
            url = join(media_path, "The Shadow Over Innsmouth.mp3")
        elif self.voc_match(phrase, "mountains_of_madness"):
            match = CPSMatchLevel.TITLE
            score += 0.7
            url = join(media_path, "At The Mountains of Madness.mp3")
        else:
            url = join(media_path, random.choice(
                ["At The Mountains of Madness.mp3",
                 "The Shadow Over Innsmouth.mp3",
                 "The Color Out of Space.mp3"
                 ]))

        if score >= 0.85:
            match = CPSMatchLevel.EXACT

        if match is not None:
            return (phrase, match, {"stream": url})
        return None

    def CPS_start(self, phrase, data):
        self.CPS_play(data["stream"])


def create_skill():
    return EpicHorrorTheatreSkill()
