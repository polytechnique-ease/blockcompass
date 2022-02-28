# Send the message to the server
async def send_sensor_msg(session, url, msg):
    # L.info("Url: %s, data: %s" % (url, msg))
    headers = {'content-type': 'application/json'}
    try:
        async with session.post(url, data=msg, headers=headers) as resp:
            if resp.status == 200:
                return True
            else:
                return False
    except:
        return False