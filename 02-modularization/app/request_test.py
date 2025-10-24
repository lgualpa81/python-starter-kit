import asyncio
import httpx
import time

URL_SYNC = "http://127.0.0.1:8000/posts/sync"
URL_ASYNC = "http://127.0.0.1:8000/posts/async"

async def hit(t, client: httpx.AsyncClient) -> tuple[float, float, dict]:
    start = time.perf_counter()
    response = await client.get(URL_ASYNC, params={"t":t})
    elapsed = time.perf_counter() - start
    return t, elapsed, response.json()

async def test_sync():
    async with httpx.AsyncClient(timeout=httpx.Timeout(20.0)) as client:
        start = time.perf_counter()
        responses = await asyncio.gather(
            client.get(URL_SYNC),
            client.get(URL_SYNC)
        )
        print("Tiempo total (sync):", time.perf_counter() - start)
        print([r.json() for r in responses])

async def test_async():
    async with httpx.AsyncClient(timeout=httpx.Timeout(20.0)) as client:
        start = time.perf_counter()
        responses = await asyncio.gather(
            client.get(URL_ASYNC),
            client.get(URL_ASYNC)
        )
        print("Tiempo total (async):", time.perf_counter() - start)
        print([r.json() for r in responses])

async def main():
    #await test_sync()
    #await test_async()
    timeout = httpx.Timeout(20.0)
    limits = httpx.Limits(max_keepalive_connections=10, max_connections=20)
    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        start = time.perf_counter()
        results = await asyncio.gather(
            hit(3.0, client),
            hit(5.5, client),
            hit(7.8, client),
            hit(9.7, client),
            return_exceptions=True
        )
        total = time.perf_counter() - start
    print("\nResults:")
    for r in results:
        if isinstance(r, Exception):
            print("Error:", repr(r))
        else:
            t, elapsed, body = r
            print(f"sleep={t:<4} tardo={elapsed:.2f}s respuesta={body}")
    print(f"\nTiempo total: {total:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())