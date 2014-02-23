import flask
import model


def app():
  app = flask.Flask('Escrow')

  @app.route('/')
  def home():
    return flask.templating.render_template('home.html')

  @app.route('/request')
  def request():
    return flask.templating.render_template('request.html')

  @app.route('/transaction')
  def fund_base():
    return flask.templating.render_template('fund.html')

  @app.route('/bounties/<category>')
  def bounties_category(category):
    return flask.templating.render_template(
        'bounties-list.html', category=category)

  @app.route('/bounties')
  def bounties_categories():
    return flask.templating.render_template('bounties.html')

  @app.route('/transaction', methods=['POST'])
  def create_transaction():
    form = flask.request.form
    transaction = model.Transaction(
        form['value'], form.get('receiver'), form['description'])
    transaction.save()
    return flask.redirect(flask.url_for(
      'fund', uuid=transaction.manage_uuid))

  @app.route('/transaction/<uuid>', methods=['GET'])
  def transaction(uuid):
    transaction = model.Transaction.get(read_uuid=uuid)
    if not transaction:
      return '', 404
    return flask.templating.render_template(
        'funded-read.html', transaction=transaction)

  @app.route('/manage/<uuid>')
  def manage(uuid):
    transaction = model.Transaction.get(manage_uuid=uuid)
    if not transaction:
      return '', 404
    return flask.templating.render_template(
        'funded-view.html', transaction=transaction)

  @app.route('/manage/<uuid>/fund')
  def fund(uuid):
    transaction = model.Transaction.get(manage_uuid=uuid)
    if not transaction:
      return '', 404
    return flask.templating.render_template(
        'fund-options.html', transaction=transaction)

  @app.route('/manage/<uuid>/fund/<option>')
  def fund_option(uuid, option):
    transaction = model.Transaction.get(manage_uuid=uuid)
    if not transaction:
      return '', 404
    transaction.in_escrow = True
    transaction.save()
    return flask.templating.render_template(
        'funded.html', transaction=transaction, option=option)

  @app.route('/manage/<uuid>/release')
  def release_funds(uuid):
    transaction = model.Transaction.get(manage_uuid=uuid)
    if not transaction:
      return '', 404
    transaction.completed = True
    transaction.save()
    return flask.templating.render_template(
        'release.html', transaction=transaction)

  @app.route('/manage/<uuid>/refund')
  def refund(uuid):
    transaction = model.Transaction.get(manage_uuid=uuid)
    if not transaction:
      return '', 404
    transaction.in_escrow = False
    transaction.save()
    return flask.templating.render_template(
        'refund.html', transaction=transaction)

  return app


def main():
  app().run(debug=True)


if __name__ == '__main__':
  main()
