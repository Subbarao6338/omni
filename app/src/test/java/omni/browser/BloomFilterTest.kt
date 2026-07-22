package omni.browser

import omni.browser.util.adblock.DefaultBloomFilter
import omni.browser.util.adblock.hash.MurmurHashStringAdapter
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class BloomFilterTest {

    @Test
    fun testBloomFilter_AddAndContain() {
        val filter = DefaultBloomFilter<String>(
            numberOfElements = 100,
            falsePositiveRate = 0.01,
            hashingAlgorithm = MurmurHashStringAdapter()
        )

        val testItems = listOf("apple", "banana", "cherry", "date", "elderberry")

        // Items shouldn't be matched before adding
        for (item in testItems) {
            assertFalse(filter.mightContain(item))
        }

        // Add single item
        filter.put("apple")
        assertTrue(filter.mightContain("apple"))
        assertFalse(filter.mightContain("banana"))

        // Add remaining items
        filter.putAll(testItems)
        for (item in testItems) {
            assertTrue(filter.mightContain(item))
        }
    }

    @Test
    fun testBloomFilter_FalsePositiveRatio() {
        val filter = DefaultBloomFilter<String>(
            numberOfElements = 1000,
            falsePositiveRate = 0.01,
            hashingAlgorithm = MurmurHashStringAdapter()
        )

        // Insert 1000 items
        val inserted = HashSet<String>()
        for (i in 0 until 1000) {
            val item = "item_$i"
            inserted.add(item)
            filter.put(item)
        }

        // Check inserted items (should always be true, zero false negatives)
        for (item in inserted) {
            assertTrue(filter.mightContain(item))
        }

        // Check false positive rate with 1000 different items
        var falsePositives = 0
        for (i in 1000 until 2000) {
            val item = "item_$i"
            if (filter.mightContain(item)) {
                falsePositives++
            }
        }

        // With falsePositiveRate = 0.01, expected false positives out of 1000 checks is around 10
        // We'll allow a generous margin for statistical variations in hashing (e.g., < 50 false positives)
        assertTrue("Too many false positives: $falsePositives", falsePositives < 50)
    }
}
