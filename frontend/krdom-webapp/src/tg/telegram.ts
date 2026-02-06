export type TgWebApp = {
  initData?: string;
  initDataUnsafe?: unknown;
  expand: () => void;
  ready: () => void;
  close: () => void;
  MainButton: {
    setText: (t: string) => void;
    show: () => void;
    hide: () => void;
    onClick: (cb: () => void) => void;
    offClick: (cb: () => void) => void;
    enable: () => void;
    disable: () => void;
  };
  themeParams?: Record<string, string>;

  openLink(url: string): void;
};

export function getTg(): TgWebApp | null {
  // @ts-expect-error Telegram WebApp injected by Telegram client
  const tg = window?.Telegram?.WebApp;
  return tg ?? null;
}

let cachedInitData: string | null = null;

export function getInitData(): string | null {
  if (cachedInitData !== null) return cachedInitData;

  // @ts-expect-error injected by Telegram
  const tg = window?.Telegram?.WebApp;
  cachedInitData = tg?.initData || null;

  console.log("initDataUnsafe =", tg?.initDataUnsafe);
  console.log("Telegram initData cached:", cachedInitData);
  return cachedInitData;
}
