export type LatestRequestGuard = {
  begin: () => number;
  cancel: () => void;
  isCurrent: (token: number) => boolean;
};

export function createLatestRequestGuard(): LatestRequestGuard;
