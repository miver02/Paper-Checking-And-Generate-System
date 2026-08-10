import asyncio
import aiohttp
import time
import random


URL = "http://172.22.5.107:30041/silver/v1/chat/completions"

API_KEY = "sk-NVl2tuQtGeHO86QixxOlWdXKukHKYbAhKUKmxeOUBosKVMuG"

CONCURRENCY = 50   # 并发数
TOTAL_REQUESTS = 200  # 总请求数


async def request(session, index):

    payload = {
        "model": "DeepSeek V4 Pro",
        "messages": [
            {
                "role": "user",
                "content": f"""
                这是第 {index} 次测试请求。

                随机编号:
                {random.randint(100000,999999)}

                请简单回答：
                你是谁？
                """
            }
        ],
        "stream": False,
        "enable_thinking": True,
        "enable_search": True
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    start = time.time()

    try:

        async with session.post(
            URL,
            json=payload,
            headers=headers,
            timeout=120
        ) as resp:

            text = await resp.text()

            cost = time.time() - start

            print(
                f"[{index}] "
                f"status={resp.status} "
                f"time={cost:.2f}s "
                f"len={len(text)}"
            )

            return {
                "ok": resp.status == 200,
                "time": cost
            }

    except Exception as e:

        cost = time.time() - start

        print(
            f"[{index}] ERROR {e} "
            f"time={cost:.2f}s"
        )

        return {
            "ok": False,
            "time": cost
        }


async def worker():

    sem = asyncio.Semaphore(CONCURRENCY)

    async with aiohttp.ClientSession() as session:

        async def run(i):

            async with sem:
                return await request(session, i)

        tasks = [
            run(i)
            for i in range(TOTAL_REQUESTS)
        ]

        return await asyncio.gather(*tasks)


if __name__ == "__main__":

    start = time.time()

    results = asyncio.run(worker())

    total = time.time()-start

    success = sum(
        1 for r in results
        if r["ok"]
    )

    avg = sum(
        r["time"]
        for r in results
    )/len(results)

    print("\n==========")
    print("总请求:", TOTAL_REQUESTS)
    print("成功:", success)
    print("失败:", TOTAL_REQUESTS-success)
    print("总耗时:", round(total, 2), "秒")
    print("平均响应:", round(avg, 2), "秒")
