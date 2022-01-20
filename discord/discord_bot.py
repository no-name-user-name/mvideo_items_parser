from discord_webhook import DiscordWebhook, DiscordEmbed
from config import webhook
from utils.decorators import catcherError


class Discord():
    """docstring for Discord"""
    def __init__(self):
        self.webhook = DiscordWebhook(url=webhook)
    
    @catcherError
    def send_message(self, item_name,item_link, img_links, item_price):
        embed = DiscordEmbed(title=item_name, url=item_link, color='3d16a2')
        embed.set_author(name='MTS monitor')
        embed.set_thumbnail(url=img_links)
        # embed.add_embed_field(name='Type', value = item_type.upper(), inline=False )
        embed.add_embed_field(name='Price', value = item_price, inline=False )
        embed.set_timestamp()
        self.webhook.add_embed(embed)
        self.webhook.execute()


