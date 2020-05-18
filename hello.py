import os
import shutil
import regex


class OrgFile:

    def __init__(self):
        self.file_list = []
        self.root_path = ""
        self.file_count_dict = {}
        print("this is a OrgFile instance")

    def iterate_dir_recursively(self):
        self.root_path = input("Please input your root_path to scan files: ")
        if not os.path.exists(self.root_path):
            print("Invalid Directory!")
            exit(1)
        self.file_list = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(self.root_path)) for f in fn]

    def extract_name_from_videos(self):
        video_list = []
        for file in self.file_list:
            if file.endswith(".mp4"):
                video_list.append(file)
        return video_list

    def extract_name_from_pics(self):
        pics_list = []
        for file in self.file_list:
            if file.endswith(".jpeg"):
                pics_list.append(file)
        return pics_list

    def make_dir(self, video_list):
        for file in video_list:
            file_sub = regex.sub(r'\.mp4$', '', os.path.basename(file))
            file_dir = os.path.join(self.root_path, file_sub)
            try:
                os.makedirs(file_dir, exist_ok=False)
                self.file_count_dict[file_dir] = 0
            except OSError:
                continue

    def move_valid_files_to_target(self, video_list, pics_list):
        extra_pics_path = os.path.join(self.root_path, "extraPics")
        for file in video_list:
            new_file_dir = os.path.join(self.root_path, regex.sub(r'\.mp4$', '', os.path.basename(file)))
            if new_file_dir in self.file_count_dict:
                update_value = self.file_count_dict.get(new_file_dir)
                print(update_value)
                self.file_count_dict.update({new_file_dir: update_value + 1})
            print(self.file_count_dict)
            shutil.move(file, os.path.join(self.root_path, regex.sub(r'\.mp4$', '', os.path.basename(file)))
                        + "/" + regex.sub(r'\.mp4$', '', os.path.basename(file)) + "_"
                        + str(self.file_count_dict.get(new_file_dir)) + ".mp4")
        for file in pics_list:
            path = os.path.join(self.root_path, regex.sub(r'\.jpeg$', '', os.path.basename(file)))
            if os.path.exists(path):
                shutil.move(file, path)
            else:
                os.makedirs(extra_pics_path, exist_ok=True)
                shutil.move(file, extra_pics_path)

    @staticmethod
    def file_util(directory):
        root_dir_list = os.listdir(directory)
        for ele in root_dir_list:
            if os.path.isdir(directory+ele):
                sub_dir_list = os.listdir(ele)
                for sub_ele in sub_dir_list:
                    if not sub_ele.startswith(".") and sub_ele.endswith("mp4"):
                        shutil.move(directory+ele+"/"+sub_ele, directory+ele+"/"+sub_ele[:-4])
        for ele in root_dir_list:
            if os.path.isdir(directory + ele):
                sub_dir_list = os.listdir(ele)
                for sub_ele in sub_dir_list:
                    if os.path.isdir(directory+ele+"/"+sub_ele):
                        shutil.move(directory+ele+"/"+sub_ele, directory)

    @staticmethod
    def remove_trash_files(directory):
        file_list = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(directory)) for f in fn]
        for file in file_list:
            if file.endswith(".torrent") or file.endswith(".js"):
                try:
                    os.remove(file)
                except OSError:
                    continue


if __name__ == "__main__":
    org_file = OrgFile()
    org_file.iterate_dir_recursively()
    new_video_list = org_file.extract_name_from_videos()
    new_pics_list = org_file.extract_name_from_pics()
    org_file.make_dir(new_video_list)
    org_file.move_valid_files_to_target(new_video_list, new_pics_list)

