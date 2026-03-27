#!/bin/bash
#
# File Organizer - Organize files by type or date
#
# Usage:
#   ./organize.sh <directory> [--by-type|--by-date|--preview]
#   ./organize.sh ~/Downloads --by-type
#   ./organize.sh ~/Downloads --by-date
#   ./organize.sh ~/Downloads --preview
#
# Options:
#   --by-type   Organize files by extension/type
#   --by-date   Organize files by modification date
#   --preview   Show what would happen without moving files

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
PREVIEW=false
BY_TYPE=false
BY_DATE=false

# File type mappings
declare -A TYPE_DIRS=(
    ["pdf"]="Documents"
    ["doc"]="Documents"
    ["docx"]="Documents"
    ["txt"]="Documents"
    ["rtf"]="Documents"
    ["odt"]="Documents"
    ["xls"]="Spreadsheets"
    ["xlsx"]="Spreadsheets"
    ["csv"]="Spreadsheets"
    ["jpg"]="Images"
    ["jpeg"]="Images"
    ["png"]="Images"
    ["gif"]="Images"
    ["svg"]="Images"
    ["webp"]="Images"
    ["bmp"]="Images"
    ["ico"]="Images"
    ["mp4"]="Videos"
    ["mov"]="Videos"
    ["avi"]="Videos"
    ["mkv"]="Videos"
    ["webm"]="Videos"
    ["mp3"]="Audio"
    ["wav"]="Audio"
    ["flac"]="Audio"
    ["aac"]="Audio"
    ["ogg"]="Audio"
    ["zip"]="Archives"
    ["tar"]="Archives"
    ["gz"]="Archives"
    ["rar"]="Archives"
    ["7z"]="Archives"
    ["py"]="Code"
    ["js"]="Code"
    ["ts"]="Code"
    ["go"]="Code"
    ["rs"]="Code"
    ["java"]="Code"
    ["cpp"]="Code"
    ["c"]="Code"
    ["h"]="Code"
    ["html"]="Code"
    ["css"]="Code"
    ["json"]="Code"
    ["yaml"]="Code"
    ["yml"]="Code"
    ["sh"]="Code"
    ["dmg"]="Installers"
    ["pkg"]="Installers"
    ["exe"]="Installers"
    ["msi"]="Installers"
    ["app"]="Installers"
)

usage() {
    echo "Usage: $0 <directory> [--by-type|--by-date|--preview]"
    echo ""
    echo "Options:"
    echo "  --by-type   Organize files by extension/type"
    echo "  --by-date   Organize files by modification date (YYYY/MM)"
    echo "  --preview   Show what would happen without moving files"
    exit 1
}

# Parse arguments
if [ $# -lt 1 ]; then
    usage
fi

TARGET_DIR="$1"
shift

while [ $# -gt 0 ]; do
    case "$1" in
        --by-type)
            BY_TYPE=true
            ;;
        --by-date)
            BY_DATE=true
            ;;
        --preview)
            PREVIEW=true
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
    shift
done

# Validate directory
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}Error: Directory not found: $TARGET_DIR${NC}"
    exit 1
fi

# Default to by-type if neither specified
if [ "$BY_TYPE" = false ] && [ "$BY_DATE" = false ]; then
    BY_TYPE=true
fi

# Get type directory for a file extension
get_type_dir() {
    local ext="${1,,}"  # lowercase
    echo "${TYPE_DIRS[$ext]:-Other}"
}

# Organize by file type
organize_by_type() {
    local dir="$1"
    local count=0

    echo -e "${GREEN}Organizing by file type...${NC}"
    echo ""

    while IFS= read -r -d '' file; do
        filename=$(basename "$file")
        ext="${filename##*.}"

        # Skip if no extension or hidden file
        if [ "$ext" = "$filename" ] || [[ "$filename" == .* ]]; then
            continue
        fi

        type_dir=$(get_type_dir "$ext")
        dest_dir="$dir/$type_dir"

        if [ "$PREVIEW" = true ]; then
            echo -e "${YELLOW}[PREVIEW]${NC} $filename -> $type_dir/"
        else
            mkdir -p "$dest_dir"
            mv "$file" "$dest_dir/"
            echo -e "${GREEN}[MOVED]${NC} $filename -> $type_dir/"
        fi

        ((count++))
    done < <(find "$dir" -maxdepth 1 -type f -print0)

    echo ""
    echo "Total files processed: $count"
}

# Organize by date
organize_by_date() {
    local dir="$1"
    local count=0

    echo -e "${GREEN}Organizing by date...${NC}"
    echo ""

    while IFS= read -r -d '' file; do
        filename=$(basename "$file")

        # Skip hidden files
        if [[ "$filename" == .* ]]; then
            continue
        fi

        # Get modification date
        if [[ "$OSTYPE" == "darwin"* ]]; then
            mod_date=$(stat -f "%Sm" -t "%Y/%m" "$file")
        else
            mod_date=$(date -r "$file" "+%Y/%m")
        fi

        dest_dir="$dir/$mod_date"

        if [ "$PREVIEW" = true ]; then
            echo -e "${YELLOW}[PREVIEW]${NC} $filename -> $mod_date/"
        else
            mkdir -p "$dest_dir"
            mv "$file" "$dest_dir/"
            echo -e "${GREEN}[MOVED]${NC} $filename -> $mod_date/"
        fi

        ((count++))
    done < <(find "$dir" -maxdepth 1 -type f -print0)

    echo ""
    echo "Total files processed: $count"
}

# Main execution
echo "========================================"
echo "File Organizer"
echo "========================================"
echo "Directory: $TARGET_DIR"
echo "Mode: $([ "$BY_TYPE" = true ] && echo "By Type" || echo "By Date")"
echo "Preview: $PREVIEW"
echo "========================================"
echo ""

if [ "$BY_TYPE" = true ]; then
    organize_by_type "$TARGET_DIR"
else
    organize_by_date "$TARGET_DIR"
fi

if [ "$PREVIEW" = true ]; then
    echo ""
    echo -e "${YELLOW}This was a preview. Run without --preview to actually move files.${NC}"
fi
