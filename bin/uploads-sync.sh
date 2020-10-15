#!/bin/sh
HOSTNAME=ddcz-access-point
TMPDIR=/tmp/ddcz-prod-sync
REMROOT=/var/www/dracidoupe.cz/www_root/www/htdocs
BUCKET="s3://uploady.dracidoupe.cz"

mkdir $TMPDIR

set -e

for dir in dobrodruzstvi soub galerie fotogalerie; do
  rsync -av w-dracidoupe-cz@ddcz-access-point:$REMROOT/$dir/ $TMPDIR/$dir/
  aws s3 sync $TMPDIR/$dir/ $BUCKET/$dir/
done;

rm -rf $TMPDIR;
