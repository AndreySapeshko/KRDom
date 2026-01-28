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
};

export function getTg(): TgWebApp | null {
  // @ts-expect-error Telegram WebApp injected by Telegram client
  const tg = window?.Telegram?.WebApp;
  return tg ?? null;
}

export function getInitData(): string | null {
  const tg = getTg();
  if (!tg) return null;
  return tg.initData || null;
}
