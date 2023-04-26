@bot.event
async def on_message(message):
    if message.author == client.user:
        return

    if len(message.attachments) > 0:
        for attachment in message.attachments:
            if attachment.content_type.endswith('image/'):
                image_data = await attachment.read()
                img = Image.open(io.BytesIO(image_data))
                texture = unitypack.utils.TextureConverter.encode_image(img)

                asset = unitypack.assets.Asset()
                asset.objects.append(unitypack.objects.Object({
                    "m_Name": "Texture",
                    "m_Texture": unitypack.objects.SerializableType(texture),
                }))

                output_file = io.BytesIO()
                output_file.write(unitypack.export.UnityAsset.to_bytes(asset))
                output_file.seek(0)

                await message.channel.send(file=discord.File(output_file, filename='items.rttex'))
