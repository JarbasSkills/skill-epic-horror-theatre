from ovos_utils.skills.templates.common_play import BetterCommonPlaySkill
from ovos_utils.playback import CPSMatchType, CPSPlayback, CPSMatchConfidence
from os.path import join, dirname


class EpicHorrorTheatreSkill(BetterCommonPlaySkill):

    def __init__(self):
        super().__init__("Epic Horror Theatre")
        self.urls = {
            "The Shadow Over Innsmouth": "https://github.com/JarbasSkills/skill-epic-horror-theatre/raw/media/media/The%20Shadow%20Over%20Innsmouth.mp3",
            "The Color Out of Space": "https://github.com/JarbasSkills/skill-epic-horror-theatre/raw/media/media/The%20Color%20Out%20of%20Space.mp3",
            "At The Mountains of Madness": "https://github.com/JarbasSkills/skill-epic-horror-theatre/raw/media/media/At%20The%20Mountains%20of%20Madness.mp3"
        }
        self.images = {
            "The Shadow Over Innsmouth": join(dirname(__file__), "ui",
                                              "innmouth.jpg"),
            "The Color Out of Space": join(dirname(__file__), "ui",
                                           "color.jpg"),
            "At The Mountains of Madness": join(dirname(__file__), "ui",
                                                "mountains.jpg")
        }
        self.supported_media = [CPSMatchType.GENERIC,
                                CPSMatchType.AUDIO,
                                CPSMatchType.AUDIOBOOK]
        self.default_bg = join(dirname(__file__), "ui", "bg.jpg")
        self.default_image = join(dirname(__file__), "ui", "logo.png")
        self.skill_logo = join(dirname(__file__), "ui", "icon.png")
        self.skill_icon = join(dirname(__file__), "ui", "icon.png")

    def get_intro_message(self):
        self.speak_dialog("intro")
        self.gui.show_image(self.logo)

    # common play
    def clean_vocs(self, phrase):
        phrase = self.remove_voc(phrase, "reading")
        phrase = self.remove_voc(phrase, "lovecraft")
        phrase = self.remove_voc(phrase, "atlanta")
        phrase = self.remove_voc(phrase, "epic_horror")
        phrase = self.remove_voc(phrase, "audio_theatre")
        phrase = self.remove_voc(phrase, "play")
        phrase = phrase.strip()
        return phrase

    # better common play
    def CPS_search(self, phrase, media_type):
        """Analyze phrase to see if it is a play-able phrase with this skill.

        Arguments:
            phrase (str): User phrase uttered after "Play", e.g. "some music"
            media_type (CPSMatchType): requested CPSMatchType to search for

        Returns:
            search_results (list): list of dictionaries with result entries
            {
                "match_confidence": CPSMatchConfidence.HIGH,
                "media_type":  CPSMatchType.MUSIC,
                "uri": "https://audioservice.or.gui.will.play.this",
                "playback": CPSPlayback.GUI,
                "image": "http://optional.audioservice.jpg",
                "bg_image": "http://optional.audioservice.background.jpg"
            }
        """
        original = phrase
        score = 0

        if self.voc_match(original, "atlanta"):
            score += 15

        if self.voc_match(original, "audio_theatre"):
            score += 35

        if self.voc_match(original, "horror"):
            score += 15
        elif self.voc_match(original, "epic_horror"):
            score += 30

        if self.voc_match(original, "lovecraft"):
            score += 50

        if media_type == CPSMatchType.AUDIOBOOK:
            score += 15

        phrase = self.clean_vocs(phrase)

        scores = {k: score for k, v in self.urls.items()}
        if self.voc_match(phrase, "color_out_of_space"):
            scores["The Color Out of Space"] += 70
            score += 70
        if self.voc_match(phrase, "innsmouth"):
            scores["The Shadow Over Innsmouth"] += 70
            score += 70
        if self.voc_match(phrase, "mountains_of_madness"):
            scores["At The Mountains of Madness"] += 70
            score += 70

        if score >= CPSMatchConfidence.AVERAGE_LOW:
            return [
                {
                    "match_confidence": min(100, scores[k]),
                    "media_type": CPSMatchType.AUDIOBOOK,
                    "uri": self.urls[k],
                    "playback": CPSPlayback.AUDIO,
                    "image": self.images[k],
                    "bg_image": self.default_bg,
                    "skill_icon": self.skill_icon,
                    "skill_logo": self.skill_logo,
                    "title": k,
                    "author": "H. P. Lovecraft"
                } for k in scores if scores[k] > 50]
        return None


def create_skill():
    return EpicHorrorTheatreSkill()
