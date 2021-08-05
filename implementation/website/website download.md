files kept
.svg
.png
.jpg

find . -type f -exec du -a {} + > size.md
:%g!/.svg\|.png\|.jpg/d
wget -E -H -k -K -p 'website'
