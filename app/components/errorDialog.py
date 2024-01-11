from flask import render_template


class ErrorDialog:
    # @staticmethod
    # def dialogDecorator(func, route = 'index'):
    #     route += '.html'
    #     # def decorator(func):
    #     def wrapper(*args, **kwargs):
    #         try:
    #             result = func(*args, **kwargs)
    #             return result
    #         except Exception as e:
    #             # Implement your error dialog logic here
    #             error_message = str(e)
    #         return render_template(route, error_message = error_message, error = True)
    #     return wrapper

    def displayErrorMessage(app):
        @app.errorhandler(Exception)
        def handleError(e):
            errorMessage = str(e)
            printErrorMessage = f"{str(e.__class__.__name__)}: {str(e)}"
            print(printErrorMessage)
            return render_template('content/errorDialog.html', errorMessage = errorMessage)

