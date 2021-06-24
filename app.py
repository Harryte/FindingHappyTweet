import flask
import tweetStream as ts
app = flask.Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))

    if flask.request.method == 'POST':
        average_time = flask.request.form['average_time']
        stream_limit = flask.request.form['stream_limit']
        print(type(average_time), type(stream_limit))

        myStreamListener = ts.MyStreamListener(
            int(average_time), int(stream_limit))
        myStream = ts.tweepy.Stream(
            auth=ts.api.auth, listener=myStreamListener)
        myStream.filter(track=[':)'])

        happiest_hashtag = ts.find_happiest_hashtag_from_list(
            myStreamListener.happy_hastag_list)

        return flask.render_template('main.html',
                                     original_input={'Average_time': average_time,
                                                     'Stream_limit': stream_limit},
                                     result=happiest_hashtag,
                                     )


if __name__ == '__main__':
    app.run()
