'''
class HistoryRouter:
    """
    A router to control all database operations on models in the
    simple_history application.
    """
    route_app_labels = {'simple_history'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read historical models go to history_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'history_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write historical models go to history_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'history_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation if a model in simple_history is involved.
        """
        if obj1._meta.app_label in self.route_app_labels or \
           obj2._meta.app_label in self.route_app_labels:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the simple_history app only appears in the 'history_db'
        database.
        """
        if app_label in self.route_app_labels:
            return db == 'history_db'
        return None
'''