import flask
import model

def app():
  app = flask.Flask('Escrow')

  @app.route('/')
  def home():
    return flask.templating.render_template('index.html')

  @app.route('/transaction', methods=['POST'])
  def create_transaction():
    form = flask.request.form
    transaction = model.Transaction(
        form['value'], form.get('receiver'), form['description'])
    transaction.save()
    return flask.redirect(flask.url_for(
      'manage', uuid=transaction.manage_uuid))

  @app.route('/transaction/<uuid>', methods=['GET'])
  def transaction(uuid):
    transaction = model.Transaction.get(read_uuid=uuid)
    return flask.templating.render_template(
        'transaction.html', transaction=transaction)

  @app.route('/manage/<uuid>')
  def manage(uuid):
    transaction = model.Transaction.get(manage_uuid=uuid)
    return flask.templating.render_template(
        'manage.html', transaction=transaction)

  return app


def main():
  app().run(debug=True)


if __name__ == '__main__':
  main()