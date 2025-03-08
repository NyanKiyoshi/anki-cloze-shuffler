from aqt import gui_hooks
from anki.cards import Card

js_sort = """

// Shuffles child nodes of a given HTML node (in-place)
function shuffleNode(node) {
    const frag = document.createDocumentFragment();
    const arr = [...node.childNodes];

    // Shuffle the array in-place (uses Sattolo's algorithm)
    let i = arr.length - 1;
    while (i > 0) {
        const j = Math.floor(Math.random() * i);
        if (j !== i) {
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        --i;
    }
    arr.forEach((el) => frag.appendChild(el));

    // Apply changes
    node.replaceChildren(frag);
}

// Shuffles all 'li' and 'ol' lists that contain cloze(s).
function shuffleAllLists() {
    document.querySelectorAll("ul:has(.cloze), ol:has(.cloze)")
        .forEach((el) => shuffleNode(el));
}

shuffleAllLists();
"""


def on_card_will_show(text: str, card: Card, kind: str) -> str:
    """
    Injects cloze javascript shuffler inside the card's HTML before rendering.
    """
    return text + f"<script>{js_sort}</script>"


gui_hooks.card_will_show.append(on_card_will_show)

