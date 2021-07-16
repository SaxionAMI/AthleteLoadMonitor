from typing import List


class MenuService:
    menu_per_role = {
        '0': [
            {'title': 'Clubs', 'path': '/home', 'icon': 'people'},
            {'title': 'Club admin', 'path': '/club-admin', 'icon': 'people'},
            {'title': 'Add club', 'path': '/add-club', 'icon': 'add'},
            {'title': 'Add club admin', 'path': '/add-club-admin', 'icon': 'add'},
        ],
        '1': [
            {'title': 'Teams', 'path': '/home', 'icon': 'people'},
            {'title': 'Players', 'path': '/team', 'icon': 'people'},
            {'title': 'Trainers', 'path': '/trainers', 'icon': 'people'},
            {'title': 'Add team', 'path': '/add-team', 'icon': 'add'},
            {'title': 'Add player', 'path': '/add-player', 'icon': 'add'},
            {'title': 'Add trainer', 'path': '/add-trainer', 'icon': 'add'},
            {'title': 'Import data', 'path': '/import', 'icon': 'upload_file'},
            {'title': 'Manage trainings', 'path': '/manage/trainings', 'icon': 'settings'},
        ],
        '2': [
            {'title': 'Teams', 'path': '/home', 'icon': 'people'},
            {'title': 'Players', 'path': '/team', 'icon': 'people'},
            {'title': 'Add player', 'path': '/add-player', 'icon': 'add'},
            {'title': 'Import data', 'path': '/import', 'icon': 'upload_file'},
        ],
    }

    def get_menu_by_role(self, role: int) -> List[dict]:
        return self.menu_per_role[str(role)]
