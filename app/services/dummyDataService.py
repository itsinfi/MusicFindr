from datetime import datetime

class DummyDataService:
    dummyUser = None

    @staticmethod
    def loadDummyData():
        """
        lädt die dummy daten.
        """
        from app.services import userService as u
        from app.services import playlistService as p

        #User erstellen, um Daten erstellen zu können
        try:
            u.UserService._createUser(27, "aBC12345!", "dummy", datetime.now(), datetime.now())
            DummyDataService.user = u.UserService.readUser(27)
        except u.UserServiceError as e:
            raise(e)
        #TODO: Jeweils einen User für uns 4?


        #Saschas Playlists erstellen
        try:
            p.PlaylistService.createPlaylist("https://music.youtube.com/playlist?list=PLnccC2viBvpEcFXJ8PsElNcQMXkOF9GP_&si=0b2bfmGW2r7awuet", "🏠🎉🏠🎉Decade of Houses Party🏠🎉🏠🎉", "Best of House (and similar genres) from the last decade:\n- Future House\n- Deep House\n- Bass House\n- Tech House\n- Speed Garage\n- UK Garage\n- UK Bassline\n- Future Bounce\n- Future Bass\n- Liquid DnB\n- Melodic Dubstep", ["House", "Future House", "Bass House", "Tech House"], 27)
        except p.PlaylistServiceError as e:
            print(e)
        try:
            p.PlaylistService.createPlaylist("https://music.youtube.com/playlist?list=PLnccC2viBvpFS8ay5RcigOGC9mOyxEhFT&si=0iCSjloMxbsIvJLK", "synthwave.", "Some great synths riding the waves of synthetically produced music...\n\nIncluding artists like:\n- The Midnight\n- The Weeknd\n- GUNSHIP\n- Greylancer\n- And many more!", ["Synthwave", "80s", "The Midnight"], 27)
        except p.PlaylistServiceError as e:
            print(e)
        try:
            p.PlaylistService.createPlaylist("https://music.youtube.com/playlist?list=PLnccC2viBvpGskcbWH0I-s04Pf1Jbdqqz&si=o1V4_8Q89dUxq6Vs", "🎱🅾 80er Hits 🎱🅾", "A compilation of all the great 80s stuff from back then!", ["80s", "80s Hits", "New Wave", "Rick Roll"], 27)
        except p.PlaylistServiceError as e:
            print(e)
        

        #Jeremys Playlists
        try:
            p.PlaylistService.createPlaylist("https://open.spotify.com/playlist/1XIzepGsQVaeSEGVqFANpU?si=dv3MysOnTeW71KyVrVoWhA&pi=e-G-sWJONURRGL", "Phonky Phonk", "A playlist of phonk tracks I listen to.", ["phonk", "drift phonk", "aggressive"], 27)
        except p.PlaylistServiceError as e:
            print(e)
        try:
            p.PlaylistService.createPlaylist("https://open.spotify.com/playlist/7H0ENzBjPTon6sL5PDVO3L?si=vIOE7LxvTKqAjWu4Mfw4sA", "💣Music to Nuke Saka Towers to💣", "A mix of loud and aggressive tracks with a certain cyberpunk-esque vibe. Perfect for mowing down corpo-henchmen or other activities in 2077.", ["industrial metal", "cyberpunk", "aggressive", "loud"], 27)
        except p.PlaylistServiceError as e:
            print(e)


        #Tijanas Playlists
        # try:
        #     p.PlaylistService.createPlaylist("https://music.youtube.com/playlist?list=PLnccC2viBvpEcFXJ8PsElNcQMXkOF9GP_&si=0b2bfmGW2r7awuet", "", "", [], 27)
        # except p.PlaylistServiceError as e:
        #     print(e)


        #Hendriks Playlists
        # try:
        #     p.PlaylistService.createPlaylist("https://music.youtube.com/playlist?list=PLnccC2viBvpEcFXJ8PsElNcQMXkOF9GP_&si=0b2bfmGW2r7awuet", "", "", [], 27)
        # except p.PlaylistServiceError as e:
        #     print(e)

        # string: str = "A passionate playlist containing some of the greatest House tracks from the last decade in the following subgenres/similar-ish genres:\n- Future House\n- Deep House\n- Bass House\n- Tech House\n- Speed Garage\n- UK Garage\n- UK Bassline\n- Future Bounce\n- Future Bass\n- Liquid DnB\n- Melodic Dubstep"
        # print(len(string))

        #Random Playlists
        try:
            p.PlaylistService.createPlaylist("https://music.youtube.com/playlist?list=PLGdEbnOoiEOOaFFYKh3A66wOUlrHUwzTs&si=UVIAjnBK03sfkyQQ", "🎉🎌INITIAL D PARTY🎌🎉", "top keks that will give an over 90% increase to your driving abilities.\n\nNOTES:\n░░█WARNING!!!!!█░░░ I AM NOT RESPONSIBLE FOR YOUR DRIVING LICENSE SUSPENSION.", ["EUROBEAT", "90s", "Initial D", "Driving"], 27)
        except p.PlaylistServiceError as e:
            print(e)
        try:
            p.PlaylistService.createPlaylist("https://music.youtube.com/playlist?list=PLCiNIjl_KpQhFwQA3G19w1nmhEOlZQsGF&si=iZrkvnFlnh9ZhCQf", "🤔🎲Roll the Rick😏😏😏", "The Ultimate Rickroll PlaylistThe Ultimate Rickroll PlaylistThe Ultimate Rickroll PlaylistThe Ultimate Rickroll PlaylistThe Ultimate Rickroll PlaylistThe Ultimate Rickroll Playlist", ["Rick Astley", "Meme", "Rick Roll", "80s"], 27)
        except p.PlaylistServiceError as e:
            print(e)

        #Inhalt printen
        # print(p.PlaylistService.allPlaylists)

        return