# from flask import Flask, render_template


# class BadAPIResponse(Exception):
#     def html(self):
#         return render_template("index_post_error.html", message="Bad API response, please try later")









# import requests
# from flask import Flask, request, jsonify 

# app = Flask(__name__)


# @app.route("/")
# def math_with_api():
#     response = requests.get("https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5")
#     a = response.json()[0] + 10
#     b = response.json()[1] + 20 
#     return jsonify( a, b)




# if __name__ == '__main__':
#     app.run(debug=True)






