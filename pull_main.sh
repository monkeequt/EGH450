#!/usr/bin/env bash
set -euo pipefail

BASE=~/catkin_ws/src

shopt -s nullglob
for gitdir in "$BASE"/*/.git; do
  repo="${gitdir%/.git}"
  name="$(basename "$repo")"

  origin_url=$(git -C "$repo" remote get-url origin 2>/dev/null || true)
  if [[ -z "$origin_url" ]]; then
    echo "[SKIP] $name: no origin remote"
    continue
  fi

  # Only operate on repos under anhadjangra/*
  if [[ ! "$origin_url" =~ ^git@github\.com:anhadjangra/[^/]+\.git$ && \
        ! "$origin_url" =~ ^https://github\.com/anhadjangra/[^/]+(\.git)?$ ]]; then
    echo "[SKIP] $name: origin is not anhadjangra (*): $origin_url"
    continue
  fi

  echo "===== $name ====="

  if [[ -n "$(git -C "$repo" status --porcelain)" ]]; then
    echo "[WARN] Working tree has uncommitted changes"
  fi

  git -C "$repo" fetch origin --prune

  # Pick branch: main preferred, fallback to master
  branch=""
  if git -C "$repo" rev-parse --verify --quiet origin/main >/dev/null; then
    branch="main"
  elif git -C "$repo" rev-parse --verify --quiet origin/master >/dev/null; then
    branch="master"
  else
    echo "[SKIP] No origin/main or origin/master found"
    continue
  fi

  # Ensure local branch exists and tracks upstream
  if git -C "$repo" rev-parse --verify --quiet "$branch" >/dev/null; then
    current_branch="$(git -C "$repo" symbolic-ref --quiet --short HEAD || echo 'DETACHED')"
    if [[ "$current_branch" != "$branch" ]]; then
      git -C "$repo" checkout "$branch"
    fi
    git -C "$repo" branch --set-upstream-to="origin/$branch" "$branch" >/dev/null 2>&1 || true
  else
    git -C "$repo" checkout -B "$branch" --track "origin/$branch"
  fi

  if git -C "$repo" pull --ff-only; then
    echo "[OK] $name: $branch is up to date."
  else
    echo "[FAIL] $name: could not fast-forward (diverged or local changes)."
  fi

  echo
done
