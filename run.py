import string
from downloader import Downloader
from prettyprinter import pprint


def show_options(downloader: Downloader):
    for index, item in enumerate(downloader.resolution):
        print(f"\t-> {[index]}: {item}")


def menu(downloader: Downloader):
    execute = True
    print("-\t" * 30)
    print("\tAvailable resolutions to download:")
    show_options(downloader)
    while execute:
        print("Your answer: ", end="\t")
        option = input("").strip()
        try:
            if type(int(option)) == int:
                print("-\t" * 30, end='\n\n')
                execute = False
                return downloader.resolution[int(option)]
        except Exception as e:
            print("\t**Invalid Input!")


if __name__ == '__main__':
    execute = True
    while (execute):
        youtube_video_link: string = input("Video LINK: ").strip()
        if (youtube_video_link):
            downloader = Downloader(youtube_video_link)

            selected_option = menu(downloader)
            print("Option= ", selected_option)

            if selected_option is not None:
                downloader.download(selected_option)

        # Exit permission from users
        ans = input('\nDo you want to Exit? (Y/N) : ')
        if ans in ['Y', 'y']:
            exit()
