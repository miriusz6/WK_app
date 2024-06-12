
import sys
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import  os
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import datetime
import time



from utils_mix.DirectoryTree import DirectoryTree, DirectoryTreeElement
from drop_box.DropBoxTree import DropBoxTree

class DB:
    def __init__(self):
        self.dropbox_path= "/wk_app_data"
        self.dropbox_log_path = "/WK_app_data/dropbox_log.txt"
        # a = os.getcwd()
        # b = os.path.join(a,'WK_app_data')
        self.local_path = os.path.join(os.getcwd(),'WK_app_data')
        self.dbx = self.log_in()
        if self.dbx is None:
            self.dbx = self.authorize_app()


    def log_in(self):
        # Check for an access token
        if not REFRESH_TOKEN:
            sys.exit("ERROR: Looks like you didn't add your access token. "
                     "Open up backup-and-restore-example.py in a text editor and "
                     "paste in your token in line 14.")
        # Create an instance of a Dropbox class, which can make requests to the API.
        print("Creating a Dropbox object...")

        # Check that the access token is valid
        try:
            dbx = dropbox.Dropbox(oauth2_refresh_token=REFRESH_TOKEN, app_key=APP_KEY, app_secret=APP_SECRET)
            dbx.users_get_current_account()
            print("Successfully logged")
            return dbx
        except AuthError:
            print(AuthError)
            return None



    def get_all_files_meta(self):
        ret = self.dbx.files_list_folder(self.dropbox_path, recursive=True, include_deleted=True)
        entries  = ret.entries

        # map(lambda e: print(e),entries)
        # for entry in entries:
        #     print(entry)

        return entries

    def init_dropbox_log(self):
        dropbox_log_local_path = os.path.join(self.local_path,self.dropbox_log_path[1:])
        curr_time_in_secs = str(time.time())
        try:
            with open(dropbox_log_local_path, "w") as f:
                f.write(curr_time_in_secs)
                print("local version of dropbox log created")
                self.dbx.files_upload(curr_time_in_secs.encode('utf-8'),
                                      self.dropbox_log_path,
                                      mode=WriteMode('overwrite'))
                print("dropbox version of dropbox log created")
        except Exception as e:
            print("Error creating dropbox log:", e)

    def download_last_modified_dropbox(self):
        modified_secs = None
        dropbox_log_local_path = os.path.join(self.local_path, self.dropbox_log_path[1:])
        a = '/' + dropbox_log_local_path.lower()
        try:
            self.dbx.files_download_to_file(download_path=dropbox_log_local_path.lower(),
                                            path=self.dropbox_log_path,
                                            )
        except Exception as err:
            print("Couldnt retrive dropbox_log",err)

        try:
            f = open(dropbox_log_local_path, "r")
            modified_secs = f.read()
        except Exception as e:
            print("Error reading local dropbox log", e)

        return modified_secs

    def upload_last_modified_dropbox(self, modified_secs):
        dropbox_log_local_path = os.path.join(self.local_path,self.dropbox_log_path[1:])
        try:
            with open(dropbox_log_local_path, "w") as f:
                f.write(modified_secs)
                self.dbx.files_upload(modified_secs.encode('utf-8'),
                                      self.dropbox_log_path,
                                      mode=WriteMode('overwrite'))
        except Exception as e:
            print("Error uploading dropbox log", e)

    def local_path_to_dropbox_path(self, local_path):
        return local_path.replace(self.local_path, self.dropbox_path).replace("\\", "/").lower()

    def dropbox_path_to_local_path(self, dropbox_path):
        return self.local_path.lower().replace(self.dropbox_path[1:],dropbox_path[1:]).replace("/", "\\")


    def update_dropbox(self):
        from utils_mix.DirectoryTree import DirectoryTree, DirectoryTreeElement
        local_tree = DirectoryTree(path_to_root=self.local_path)
        dropbox_files = self.get_all_files_meta()
        dropbox_files = [f for f in dropbox_files if not isinstance(f, dropbox.files.DeletedMetadata)]

        for local_file in local_tree.get_all_nodes():
            found = False
            local_path = self.local_path_to_dropbox_path(local_file.full_path)
            for online_meta in dropbox_files:
                if online_meta.path_lower == local_path:
                    found = True
                    dropbox_files.pop(dropbox_files.index(online_meta))
                    print("found online:", online_meta.path_lower)
            if not found:
                print("not found online:", local_path, "\n uploading")
                self.upload_file(local_path, local_file.full_path)
        dropbox_files.sort(key=lambda x: len(x.path_lower), reverse=True)
        # needs to be optimized, so it deletes whole dirs first
        for to_delete in dropbox_files:
            print("deleting online:", to_delete.path_lower)
            try:
                self.delete(to_delete)
            except Exception as e:
                print("Error deleting file(parent folder could be deleted):", e)


    #def update_client_dir(self, dir:dropbox.files.FolderMetadata):




    def update_client(self):
        from utils_mix.DirectoryTree import DirectoryTree, DirectoryTreeElement
        local_tree = DirectoryTree(path_to_root=self.local_path)
        dropbox_files = self.get_all_files_meta()
        dropbox_files = [f for f in dropbox_files if not isinstance(f, dropbox.files.DeletedMetadata)]

        local_files = local_tree.get_all_nodes()
        local_files.sort(key=lambda x: len(x.full_path), reverse=True)
        dropbox_files.sort(key=lambda x: len(x.path_lower), reverse=True)

        # if dont match then:
        #   dropbox have a new one so it cant be found by iterating
        #       download
        #   local have a new one so it can be found by iterating
        #       to delete
        j = 0
        for i in range(len(dropbox_files)):
            found = False
            online_path = self.dropbox_path_to_local_path(dropbox_files[i].path_lower)
            offset = 0
            for local_file in local_files[j:]:
                if local_file.full_path.lower() == online_path:
                    found = True
                    print("found locally:", online_path)
                    local_files.pop(local_files.index(local_file))
                    break
                else:
                    offset += 1
            if not found:
                print("downloading: ",online_path)
                pass # download
            else:
                for to_delete in local_files[j:j+offset]:
                    print("deleting:",to_delete.full_path.lower())
                # delete local_files[j:j+offset]
                j += offset



    def scan_local(self):
        local_tree = DirectoryTree(path_to_root=self.local_path)
        online_tree = DropBoxTree(self.get_all_files_meta())
        delete, down = self.__scan_local_node(online_tree.root, local_tree.root)
        print("to delete:",delete,"\n to download:",down)
        return

    def __scan_local_node(self, target_node, other_node):
        to_delete = []
        to_download = []
        if target_node.full_name != other_node.full_name.lower():
            return ([target_node],[])

        target_children = target_node.children.copy()
        other_children = other_node.children.copy()

        for target in target_children:
            found = False
            for other in other_children:
                if target.full_name == other.full_name.lower():
                    found = True
                    to_delete, to_download = self.__scan_local_node(target, other)
                    to_delete.extend(to_delete)
                    to_download.extend(to_download)
                    other_children.pop(other_children.index(other))
                    break
            if not found:
                to_download.append(target)
        to_delete.extend(other_children)
        to_download.extend(target_children)
        return to_delete, to_download





        # for online_meta in dropbox_files:
        #     found = False
        #     online_path = self.dropbox_path_to_local_path(online_meta.path_lower)
        #     for local_file in local_files:
        #         if local_file.full_path.lower() == online_path:
        #             found = True
        #             print("found locally:", local_file.full_path)
        #             local_files.pop(local_files.index(local_file))
        #     if not found:
        #         print("not found locally:", online_meta.path_lower, "\n downloading")
        #         self.update_local(online_meta)
        # # needs to be optimized, so it deletes whole dirs first
        # for to_delete in local_files:
        #     print("deleting locally:", to_delete.path_lower)
        #     try:
        #         pass
        #         #os.remove(to_delete.full_path)
        #     except Exception as e:
        #         print("Error deleting file(parent folder could be deleted):", e)
        # for online_meta in dropbox_files:
        #     found = False
        #     online_path = self.dropbox_path_to_local_path(online_meta.path_lower)
        #     for local_file in local_files:
        #         if local_file.full_path.lower() == online_path:
        #             found = True
        #             print("found locally:", local_file.full_path)
        #             local_files.pop(local_files.index(local_file))
        #     if not found:
        #         print("not found locally:", online_meta.path_lower, "\n downloading")
        #         self.update_local(online_meta)
        # # needs to be optimized, so it deletes whole dirs first
        # for to_delete in local_files:
        #     print("deleting locally:", to_delete.path_lower)
        #     try:
        #         pass
        #         #os.remove(to_delete.full_path)
        #     except Exception as e:
        #         print("Error deleting file(parent folder could be deleted):", e)


    def update_local(self, f_meta: dropbox.files.FileMetadata):
        """
               Starts returning the contents of a folder. If the result's
               ``ListFolderResult.has_more`` field is ``True``, call
               :meth:`files_list_folder_continue` with the returned
               ``ListFolderResult.cursor`` to retrieve more entries.
               If you're using
               ``ListFolderArg.recursive`` set to ``True`` to keep a local cache of the
               contents of a Dropbox account, iterate through each entry in order and
               process them as follows to keep your local state in sync:
               For each:class:`dropbox.files.FileMetadata`, store the new entry at the given
               path in your local state.

               If the required parent folders don't exist
                yet, create them. If there's already something else at the given path,
               replace it and remove all its children.
               store the new entry at the given at path in your local state.
               If the required parent folders don't exist
               yet, create them.
               If there's already something else at the given path,
               replace it but leave the children as they are.
               Check the new entry's
               ``FolderSharingInfo.read_only`` and set all its children's read-only
               statuses to match.
               For each :class:`dropbox.files.DeletedMetadata`, if
               your local state has something at the given path, remove it and all its
               children. If there's nothing at the given path, ignore this entry.
                Note:
               :class:`dropbox.auth.RateLimitError` may be returned if multiple
               :meth:`files_list_folder` or :meth:`files_list_folder_continue` calls
               with same parameters are made simultaneously by same API app for same
               user. If your app implements retry logic, please hold off the retry
               until the previous request finishes."""
        #local_p = os.path.join(self.local_path, f_meta.path_lower)
        local_p = self.dropbox_path_to_local_path(f_meta.path_lower)
        is_deleted = isinstance(f_meta, dropbox.files.DeletedMetadata)
        is_dir = isinstance(f_meta, dropbox.files.FolderMetadata)
        is_file = isinstance(f_meta, dropbox.files.FileMetadata)
        exists = os.path.exists(local_p)
        if is_deleted:
            return
        # dir
        if is_dir and not exists:
            print("Creating folder: ", f_meta.name)
            os.makedirs(local_p)
            return
        # file
        if exists and is_file:
            online_time = f_meta.server_modified
            # create datetime object from the timestamp
            online_time = datetime.datetime.fromtimestamp(online_time)
            # get the modification time of the file
            local_time = os.path.getmtime(local_p)
            # create datetime object from the timestamp
            local_time = datetime.datetime.fromtimestamp(local_time)
            # compare the modification times
            if online_time > local_time:
                # download the file
                self.download_file(f_meta, local_p)
            else:
                # upload the file
                self.upload_file(local_p, local_p)
        elif not exists and is_file:
            self.download_file(f_meta, local_p)



    def download_file(self, f_meta: dropbox.files.FileMetadata, local_p):
        print("Downloading file: ", f_meta.name)
        self.dbx.files_download_to_file(local_p, f_meta.path_lower)

    # def upload_file(self, f_meta: dropbox.files.FileMetadata, local_p):
    #     print("Uploading file: ", f_meta.name)
    #     with open(local_p, 'rb') as f:
    #         self.dbx.files_upload(f.read(), f_meta.path_lower, mode=WriteMode('overwrite'))

    def upload_file(self, dropbox_path: str, local_p):
        print("Uploading file: ", dropbox_path)
        if os.path.isdir(local_p):
            self.dbx.files_create_folder_v2(dropbox_path)
            return
        with open(local_p, 'rb') as f:
            self.dbx.files_upload(f.read(),dropbox_path, mode=WriteMode('overwrite'))

    def delete(self, f_meta: dropbox.files.FileMetadata):
        print("Deleting file: ", f_meta.name)
        # deletes a file or folder
        self.dbx.files_delete_v2(f_meta.path_lower)

    def create_folder(self, f_meta: dropbox.files.FolderMetadata):
        print("Creating folder: ", f_meta.name)
        # creates a folder
        self.dbx.files_create_folder_v2(f_meta.path_lower)

    def move(self, f_meta: dropbox.files.FileMetadata, new_path):
        print("Moving file: ", f_meta.name)
        # moves a file or folder
        self.dbx.files_move_v2(f_meta.path_lower, new_path)

    def copy(self, f_meta: dropbox.files.FileMetadata, new_path):
        print("Copying file: ", f_meta.name)
        # copies a file or folder
        self.dbx.files_copy_v2(f_meta.path_lower, new_path)


    # dbx: dropbox.dropbox_client.Dropbox = log_in()
    # meta = dbx.files_get_metadata(BACKUPPATH)
    # print(meta)

    # def is_up_to_date(self, file_path):
    #     # Get the metadata for the file
    #     print("Getting metadata from Dropbox...")
    #     file = self.dbx.files_get_metadata(BACKUPPATH)
    #
    #     # Check the modified times of the two files to see if the local file is newer
    #     print("Comparing " + file_path + " to " + BACKUPPATH + "...")
    #     if os.stat(file_path).st_mtime > time_to_seconds(file.server_modified, is_zulu=True):
    #         print("File is up to date.")
    #         return True
    #     print("File is not up to date.")
    #     return False

    def authorize_app(self):

        '''
        This example walks through a basic oauth flow using the existing long-lived token type
        Populate your app key and app secret in order to run this locally
        '''
        auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET,token_access_type = 'offline')

        authorize_url = auth_flow.start()
        print("1. Go to: " + authorize_url)
        print("2. Click \"Allow\" (you might have to log in first).")
        print("3. Copy the authorization code.")
        auth_code = input("Enter the authorization code here: ").strip()

        try:
            oauth_result = auth_flow.finish(auth_code)
        except Exception as e:
            print('Error: %s' % (e,))
            exit(1)

        try:
            dbx = dropbox.Dropbox(oauth2_access_token=oauth_result.access_token)
            dbx.users_get_current_account()
            print("Successfully set up client!: ", oauth_result.access_token)
            return dbx
        except Exception as e:
            print("Error setting up client: " , e)
            return None



db = DB()

db.scan_local()

from drop_box.DropBoxTree import DropBoxTree

#tree =  DropBoxTree(db.get_all_files_meta())
#tree.print_extracted()
#tree.print_tree()
#print(tree.RET)
#tree.print_tree()


#db.init_dropbox_log()
# t1 = db.download_last_modified_dropbox()
# t2 = db.download_last_modified_dropbox()
# print("first time:",t1)
# print("second time:",t2)
#db.update_dropbox()


# DROP_PATH =  '/wk_app_data/dropbox_log.txt'
# LOCAL_PATH =  '\\wk_app_data\dropbox_log.txt'
#
# print(db.local_path_to_dropbox_path(LOCAL_PATH))
# print(db.dropbox_path_to_local_path(DROP_PATH))

#files = db.get_all_files_meta()
#db.last_modified_dropbox(files)

#
# db.dbx.file
# db.dbx.files_list_folder_longpoll()
#db.update_client()
#print(db.dropbox_path_to_local_path('/wk_app_data/dropbox_log.txt'))
#os.makedirs()

import re


# '/wk_app_data'
# 'C:\\felt_WK_app\\drop_box\\WK_app_data'
#'c:\\felt_wk_app\\drop_box\\wk_app_data'
#
# d = '/wk_app_data/dropbox_log.txt'
# l = 'C:\\felt_WK_app\\drop_box\\WK_app_data'
# l = l.lower()
#
# ret = re.sub('wk_app_data', d[1:], l)
# print(ret)
# print(l.replace('wk_app_data', d[1:]))
# print("KUPA")


def seconds_to_time(seconds, is_zulu=False):
    if is_zulu:
        return time.gmtime(seconds)
    return time.ctime(seconds)

def time_to_seconds(time_str, is_zulu=False):
    if is_zulu:
        return time.mktime(time.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ"))
    return time.mktime(time.strptime(time_str))


# save last sync date
# if last sync newer than server last modified update drop
# else update local

