#from db_func import *
import pandas as pd
from dagster import asset, AssetKey, EnvVar
from dagster import HookContext, failure_hook, success_hook
from dagster_airbyte import airbyte_resource, load_assets_from_airbyte_instance#, load_assets_from_connections

from ..constants import AIRBYTE_CONNECTION_ID, DBT_PROJECT_DIR, AIRBYTE_CONFIG

@failure_hook()
def message_on_failure(context: HookContext):
    message = f'''{context.job_name} - {context.op.name} failed
               <p>Ошикба: {context.op_exception}</p>'''
    send_mail_new(message,subject=f'Ошибка {context.job_name}',to_emails='vladimir.petryakov@rt.ru')

    bot_oao_dagster.send_message(chat_dagster_oao, str(datetime.datetime.now().strftime("<u>%Y-%m-%d %H:%M </u>\n<b>"))+message.replace('<p>','</b>\n<i>').replace('</p>','</i>'),parse_mode='html')

airbyte_instance = airbyte_resource.configured(AIRBYTE_CONFIG)
#airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance, connection_to_asset_key_fn=lambda c, n: AssetKey([c.name, n]), key_prefix=["staging"])

airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance, key_prefix=["raw"])
#airbyte_assets = load_assets_from_connections(airbyte=airbyte_instance, connections=[cereals_connection])