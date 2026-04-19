#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def replace_once(text: str, old: str, new: str, relpath: str) -> str:
    if old not in text:
        fail(f"Expected snippet not found in {relpath}: {old[:120]!r}")
    return text.replace(old, new, 1)


def main() -> None:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()

    helper_rel = "src/lib/chinaFriendlyGeo.ts"
    helper_path = root / helper_rel
    helper_content = """const taiwanNameMap: Record<string, string> = {
  'ar': 'تايوان، الصين',
  'bg': 'Тайван, Китай',
  'bn': 'তাইওয়ান, চীন',
  'ca': 'Taiwan, Xina',
  'cs': 'Tchaj-wan, Čína',
  'da': 'Taiwan, Kina',
  'de': 'Taiwan, China',
  'el': 'Ταϊβάν, Κίνα',
  'en': 'Taiwan, China',
  'es': 'Taiwán, China',
  'et': 'Taiwan, Hiina',
  'fa': 'تایوان، چین',
  'fi': 'Taiwan, Kiina',
  'fr': 'Taïwan, Chine',
  'he': 'טייוואן, סין',
  'hi': 'ताइवान, चीन',
  'hr': 'Tajvan, Kina',
  'hu': 'Tajvan, Kína',
  'id': 'Taiwan, Tiongkok',
  'it': 'Taiwan, Cina',
  'ja': '中国台湾',
  'ko': '중국 대만',
  'lt': 'Taivanas, Kinija',
  'lv': 'Taivāna, Ķīna',
  'ms': 'Taiwan, China',
  'nb': 'Taiwan, Kina',
  'nl': 'Taiwan, China',
  'pl': 'Tajwan, Chiny',
  'pt': 'Taiwan, China',
  'ro': 'Taiwan, China',
  'ru': 'Тайвань, Китай',
  'sk': 'Taiwan, Čína',
  'sl': 'Tajvan, Kitajska',
  'sr': 'Тајван, Кина',
  'sv': 'Taiwan, Kina',
  'ta': 'தைவான், சீனா',
  'th': 'ไต้หวัน, จีน',
  'tr': 'Tayvan, Çin',
  'uk': 'Тайвань, Китай',
  'ur': 'تائیوان، چین',
  'vi': 'Đài Loan, Trung Quốc',
  'zh': '中国台湾',
};

export function getChinaFriendlyTaiwanName(locale: string): string {
  const normalized = (locale || '').toLowerCase();
  const base = normalized.split('-')[0];

  if (normalized === 'zh-cn' || normalized === 'zh-sg') {
    return '中国台湾';
  }

  if (normalized === 'zh-tw' || normalized === 'zh-hk' || normalized === 'zh-mo') {
    return '中國台灣';
  }

  return taiwanNameMap[normalized] || taiwanNameMap[base] || 'Taiwan, China';
}

export function applyChinaFriendlyCountryNames(
  locale: string,
  input: Record<string, string>,
): Record<string, string> {
  return {
    ...input,
    TW: getChinaFriendlyTaiwanName(locale),
  };
}

export function mapChinaFriendlyCountryCodeForFlag(code?: string): string | undefined {
  if (code === 'TW') {
    return 'CN';
  }

  return code;
}

export function mapChinaFriendlyTypeIconValue(type: string, value?: string): string {
  if (type === 'country') {
    return mapChinaFriendlyCountryCodeForFlag(value) || 'unknown';
  }

  return value || 'unknown';
}
"""
    write_text(helper_path, helper_content)

    # Patch useCountryNames.ts
    rel = "src/components/hooks/useCountryNames.ts"
    path = root / rel
    text = read_text(path)
    if "chinaFriendlyGeo" not in text:
        text = replace_once(
            text,
            "import { httpGet } from '@/lib/fetch';\n",
            "import { httpGet } from '@/lib/fetch';\nimport { applyChinaFriendlyCountryNames } from '@/lib/chinaFriendlyGeo';\n",
            rel,
        )
        text = replace_once(
            text,
            "const [list, setList] = useState(countryNames[locale] || enUS);",
            "const [list, setList] = useState(applyChinaFriendlyCountryNames(locale, countryNames[locale] || enUS));",
            rel,
        )
        text = replace_once(
            text,
            "      setList(countryNames[locale]);",
            "      setList(applyChinaFriendlyCountryNames(locale, countryNames[locale]));",
            rel,
        )
        text = replace_once(
            text,
            "      setList(enUS);",
            "      setList(applyChinaFriendlyCountryNames(locale, enUS));",
            rel,
        )
        text = replace_once(
            text,
            "      setList(countryNames[locale]);",
            "      setList(applyChinaFriendlyCountryNames(locale, countryNames[locale]));",
            rel,
        )
        write_text(path, text)

    # Patch TypeIcon.tsx
    rel = "src/components/common/TypeIcon.tsx"
    path = root / rel
    text = read_text(path)
    if "mapChinaFriendlyTypeIconValue" not in text:
        text = replace_once(
            text,
            "import { Row } from '@umami/react-zen';\n",
            "import { Row } from '@umami/react-zen';\nimport { mapChinaFriendlyTypeIconValue } from '@/lib/chinaFriendlyGeo';\n",
            rel,
        )
        text = replace_once(
            text,
            "          value?.replaceAll(' ', '-').toLowerCase() || 'unknown'\n",
            "          mapChinaFriendlyTypeIconValue(type, value).replaceAll(' ', '-').toLowerCase()\n",
            rel,
        )
        write_text(path, text)

    # Patch MetricLabel.tsx
    rel = "src/components/metrics/MetricLabel.tsx"
    path = root / rel
    text = read_text(path)
    if "mapChinaFriendlyCountryCodeForFlag" not in text:
        text = replace_once(
            text,
            "import { GROUPED_DOMAINS } from '@/lib/constants';\n",
            "import { GROUPED_DOMAINS } from '@/lib/constants';\nimport { mapChinaFriendlyCountryCodeForFlag } from '@/lib/chinaFriendlyGeo';\n",
            rel,
        )
        text = replace_once(
            text,
            "                  country?.toLowerCase() || 'xx'\n",
            "                  mapChinaFriendlyCountryCodeForFlag(country)?.toLowerCase() || 'xx'\n",
            rel,
        )
        text = replace_once(
            text,
            "                alt={country}\n",
            "                alt={mapChinaFriendlyCountryCodeForFlag(country) || country}\n",
            rel,
        )
        write_text(path, text)

    print("CN patch applied successfully.")


if __name__ == "__main__":
    main()
