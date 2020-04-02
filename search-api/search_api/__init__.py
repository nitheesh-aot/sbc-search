# Copyright © 2020 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dotenv import load_dotenv
import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import exc

from search_api import config
from search_api.auth import jwt
from search_api.resources import DIRECTORS_API, BUSINESSES_API
from search_api.models import db

load_dotenv(verbose=True)


def create_app(run_mode=os.getenv("FLASK_ENV", "production")):
    """Return a configured Flask App using the Factory method."""

    app = Flask(__name__)
    app.config.from_object(config.CONFIGURATION[run_mode])

    db.init_app(app)
    migrate = Migrate(app, db)

    CORS(app)

    # Configure Sentry
    if app.config.get("SENTRY_DSN", None):
        sentry_sdk.init(
            dsn=app.config.get("SENTRY_DSN"), integrations=[FlaskIntegration()]
        )

    app.register_blueprint(DIRECTORS_API)
    app.register_blueprint(BUSINESSES_API)

    setup_jwt_manager(app, jwt)

    @app.route("/ops/readyz")
    def readyz():
        return {'message': 'api is ready'}, 200

    @app.route("/ops/healthz")
    def healthz():
        """Return a JSON object stating the health of the Service and dependencies."""
        try:
            db.engine.execute('SELECT 1 FROM CORP_PARTY')
        except exc.SQLAlchemyError:
            return {'message': 'api is down'}, 500

        # made it here, so all checks passed
        return {'message': 'api is healthy'}, 200

    return app


def setup_jwt_manager(app, jwt_manager):
    """Use flask app to configure the JWTManager to work for a particular Realm."""
    def get_roles(a_dict):
        return a_dict['realm_access']['roles']  # pragma: no cover
    app.config['JWT_ROLE_CALLBACK'] = get_roles

    jwt_manager.init_app(app)
