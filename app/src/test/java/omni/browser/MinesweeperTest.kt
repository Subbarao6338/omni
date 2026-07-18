package omni.browser

import org.junit.Assert.*
import org.junit.Test
import omni.toolbox.ui.screens.lifestyle.generateMinesweeper
import omni.toolbox.ui.screens.lifestyle.revealMinesweeper

class MinesweeperTest {

    @Test
    fun testGenerateMinesweeper_correctSizeAndMineCount() {
        val size = 8
        val mineCount = 10
        val board = generateMinesweeper(size, mineCount)

        // Verify board dimensions
        assertEquals(size, board.size)
        for (row in board) {
            assertEquals(size, row.size)
        }

        // Verify correct mine count and that all other cells contain correct neighbor counts
        var actualMineCount = 0
        for (r in 0 until size) {
            for (c in 0 until size) {
                if (board[r][c] == -1) {
                    actualMineCount++
                } else {
                    // Check neighbors
                    var expectedCount = 0
                    for (dr in -1..1) {
                        for (dc in -1..1) {
                            val nr = r + dr
                            val nc = c + dc
                            if (nr in 0 until size && nc in 0 until size && board[nr][nc] == -1) {
                                expectedCount++
                            }
                        }
                    }
                    assertEquals("Mismatch at ($r, $c)", expectedCount, board[r][c])
                }
            }
        }
        assertEquals(mineCount, actualMineCount)
    }

    @Test
    fun testRevealMinesweeper_singleCellReveal() {
        val size = 3
        // Create a custom board:
        //  0  1 -1
        //  0  1  1
        //  0  0  0
        val board = arrayOf(
            intArrayOf(0, 1, -1),
            intArrayOf(0, 1, 1),
            intArrayOf(0, 0, 0)
        )

        // Clicking on a cell with neighbor count (e.g., at (1, 1)) should only reveal that cell
        val revealed = revealMinesweeper(board, emptySet(), 1, 1, size)
        assertEquals(setOf(1 to 1), revealed)
    }

    @Test
    fun testRevealMinesweeper_floodFillReveal() {
        val size = 3
        // Create a custom board with a 0 cell at (1, 0)
        // -1  1  0
        //  1  1  0
        //  0  0  0
        val board = arrayOf(
            intArrayOf(-1, 1, 0),
            intArrayOf(1, 1, 0),
            intArrayOf(0, 0, 0)
        )

        // Revealing at (2, 2) which is a 0 should cascade to neighbors.
        // It should reveal (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 1) etc.
        // Let's test revealing (2, 2) which is 0.
        val revealed = revealMinesweeper(board, emptySet(), 2, 2, size)

        // The cells expected to be revealed:
        // (2, 2) [0] -> triggers neighbors:
        // (1, 1) [1], (1, 2) [0], (2, 1) [0]
        // (1, 2) [0] -> triggers neighbors:
        // (0, 1) [1], (0, 2) [0], (1, 1) [1], (1, 2) [0], (2, 2) [0], (2, 1) [0]
        // (0, 2) [0] -> triggers neighbors:
        // (0, 1) [1], (0, 2) [0], (1, 1) [1], (1, 2) [0]
        // (2, 1) [0] -> triggers neighbors:
        // (1, 0) [1], (1, 1) [1], (1, 2) [0], (2, 0) [0], (2, 1) [0], (2, 2) [0]
        // (2, 0) [0] -> triggers neighbors:
        // (1, 0) [1], (1, 1) [1], (2, 0) [0], (2, 1) [0]
        // So cells (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2) are all revealed.
        // Essentially everything except (-1 at (0, 0)) is revealed.
        assertTrue(revealed.contains(2 to 2))
        assertTrue(revealed.contains(1 to 2))
        assertTrue(revealed.contains(0 to 2))
        assertTrue(revealed.contains(0 to 1))
        assertTrue(revealed.contains(1 to 1))
        assertTrue(revealed.contains(2 to 1))
        assertTrue(revealed.contains(2 to 0))
        assertTrue(revealed.contains(1 to 0))
        assertFalse(revealed.contains(0 to 0))
        assertEquals(8, revealed.size)
    }

    @Test
    fun testRevealMinesweeper_outOfBoundsAndAlreadyRevealed() {
        val size = 3
        val board = arrayOf(
            intArrayOf(0, 0, 0),
            intArrayOf(0, 0, 0),
            intArrayOf(0, 0, 0)
        )

        // Out of bounds r or c should return original revealed set unchanged
        val initial = setOf(1 to 1)
        assertEquals(initial, revealMinesweeper(board, initial, -1, 0, size))
        assertEquals(initial, revealMinesweeper(board, initial, 0, -1, size))
        assertEquals(initial, revealMinesweeper(board, initial, 3, 0, size))
        assertEquals(initial, revealMinesweeper(board, initial, 0, 3, size))

        // Already revealed cell should return original revealed set unchanged
        assertEquals(initial, revealMinesweeper(board, initial, 1, 1, size))
    }
}
