import tkinter as tk
import tkinter.scrolledtext as tkst
import video_library as lib
from font_manager import configure

def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", content)

class VideoPlayer:
    def __init__(self, window):
        self.window = window
        self.window.geometry("800x700")
        self.window.title("Video Player")
        self.window.configure(bg='cyan')
        configure()

        # CHECK VIDEOS
        list_all_videos_button = tk.Button(self.window, text="List All Videos", command=self.list_videos_clicked)
        list_all_videos_button.grid(row=0, column=0, padx=10, pady=10)

        self.enter_video_number_label = tk.Label(self.window, text="Enter Video Number", bg='cyan')
        self.enter_video_number_label.grid(row=0, column=1, padx=10, pady=10)

        self.enter_video_number = tk.Entry(self.window, width=3)
        self.enter_video_number.grid(row=0, column=2, padx=10, pady=10)

        self.check_video_button = tk.Button(self.window, text="Check Video", command=self.check_video_clicked)
        self.check_video_button.grid(row=0, column=3, padx=10, pady=10)

        self.video_info_text = tkst.ScrolledText(self.window, width=80, height=10, wrap="none")
        self.video_info_text.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # CREATE VIDEO LIST
        self.playlist_text = tkst.ScrolledText(self.window, width=80, height=5, wrap="none")
        self.playlist_text.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        add_to_playlist_button = tk.Button(self.window, text="Add to Playlist", command=self.add_to_playlist_clicked)
        add_to_playlist_button.grid(row=2, column=0, padx=10, pady=10)

        play_playlist_button = tk.Button(self.window, text="Play Playlist", command=self.play_playlist_clicked)
        play_playlist_button.grid(row=2, column=1, padx=10, pady=10)

        reset_playlist_button = tk.Button(self.window, text="Reset Playlist", command=self.reset_the_playlist_clicked)
        reset_playlist_button.grid(row=2, column=2, padx=10, pady=10)

        # UPDATE VIDEOS
        update_rating_label = tk.Label(self.window, text="Enter New Rating", bg='cyan')
        update_rating_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.rating_entry = tk.Entry(self.window, width=5)
        self.rating_entry.grid(row=3, column=1, padx=10, pady=5)

        update_button = tk.Button(self.window, text="Update", command=self.update_clicked)
        update_button.grid(row=3, column=2, padx=10, pady=5)

        self.status_lbl = tk.Label(self.window, text="", font=("Helvetica", 10), bg='cyan')
        self.status_lbl.grid(row=4, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        # SEARCH VIDEOS BY NAME
        search_label = tk.Label(self.window, text="Search by Name", bg='cyan')
        search_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.search_entry = tk.Entry(self.window, width=20)
        self.search_entry.grid(row=4, column=1, padx=10, pady=5)

        search_button = tk.Button(self.window, text="Search", command=self.search_clicked)
        search_button.grid(row=4, column=2, padx=10, pady=5)

        # FILTER
        self.director_label = tk.Label(self.window, text="Select Director", bg='cyan')
        self.director_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        self.filter_entry = tk.Entry(self.window, text="Filter by Director")
        self.filter_entry.grid(row=7, column=1, padx=10, pady=5)

    # CHECK VIDEOS FUNCTIONS
    def check_video_clicked(self):
        key = self.enter_video_number.get()
        video = lib.library.get(key)
        
        if video is not None:
            director = video.director
            rating = video.rating
            play_count = video.play_count
            
            video_details = f"Name: {video.name}\nDirector: {director}\nRating: {rating}\nPlay Count: {play_count}"
            set_text(self.video_info_text, video_details)
        else:
            set_text(self.video_info_text, f'Video {key} not found')

    def list_videos_clicked(self):
        video_list = lib.list_all()
        set_text(self.video_info_text, video_list)

    # CREATE VIDEO LIST FUNCTIONS
    def add_to_playlist_clicked(self):
        key = self.enter_video_number.get()
        name = lib.get_name(key)
        if name is not None:
            video_details = f"{name}\n"
            self.playlist_text.insert("end", video_details)
        else:
            set_text(self.playlist_text, f"Video {key} not found")

    def play_playlist_clicked(self):
        key = self.enter_video_number.get()
        name = lib.get_name(key)
        if name is not None:
            play_count = lib.increment_play_count(key)
            video_details = f"{name}: {play_count}"
            set_text(self.playlist_text, video_details)

    def reset_the_playlist_clicked(self):
        key = self.enter_video_number.get()
        name = lib.get_name(key)
        if name is not None:
            self.playlist_text.delete("1.0", tk.END)
            lib.library[key].play_count = 0

    # UPDATE VIDEO FUNCTIONS
    def update_clicked(self):
        key = self.enter_video_number.get()
        video = lib.library.get(key)
        video_number = self.enter_video_number.get()
        new_rating = self.rating_entry.get()
        if video is not None:
            if not new_rating.isdigit():
                self.set_video_info_text("Invalid rating!")
                return
            new_rating = int(new_rating)
            if 1 <= new_rating <= 5:
                lib.set_rating(video_number, new_rating)
                video_name = lib.get_name(video_number)
                play_count = lib.get_play_count(video_number)
                update_message = f"Updated: {video_name} (Rating: {new_rating}, Plays: {play_count})"
                self.set_video_info_text(update_message)
            else:
                self.set_video_info_text("Rating should be between 1 and 5!")
        else:
            set_text(self.video_info_text, f'Video {key} not found')



        

    def set_video_info_text(self, message):
        self.video_info_text.delete("1.0", tk.END)
        self.video_info_text.insert("1.0", message)

    # SEARCH VIDEOS BY NAME FUNCTIONS
    def search_clicked(self):
        search_term = self.search_entry.get()
        search_result = self.perform_search(search_term)
        if search_result:
            set_text(self.video_info_text, search_result)
        else:
            set_text(self.video_info_text, f"No results found for '{search_term}'")

    def perform_search(self, search_term):
        search_result = []
        for key in lib.library:
            name = lib.get_name(key)
            director = lib.get_director(key)
            if search_term.lower() in name.lower() or search_term.lower() in director.lower():
                rating = lib.get_rating(key)
                play_count = lib.get_play_count(key)
                video_details = f"Name: {name}\nDirector: {director}\nRating: {rating}\nPlay Count: {play_count}\n"
                search_result.append(video_details)
        return "\n\n".join(search_result)
    
    # FILTER FUNCTIONS




# MAIN PROGRAM
if __name__ == "__main__":
    window = tk.Tk()
    VideoPlayer(window)
    window.mainloop()
