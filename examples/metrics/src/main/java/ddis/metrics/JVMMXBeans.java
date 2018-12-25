package ddis.metrics;

import java.lang.management.ManagementFactory;
import java.lang.management.ThreadMXBean;

public class JVMMXBeans {

    public static void threadMXBean() throws Exception {
        ThreadMXBean threadMXBean = ManagementFactory.getThreadMXBean();
        boolean cpuTimeSupported = threadMXBean.isCurrentThreadCpuTimeSupported();
        long startTime = System.currentTimeMillis();
        long startCpu = threadMXBean.getCurrentThreadCpuTime();
        Thread.sleep(5 * 1000);
        long endCpu = threadMXBean.getCurrentThreadCpuTime();
        long endTime = System.currentTimeMillis();
        System.out.println("cpuTimeSupported = " + cpuTimeSupported);
        System.out.println("cpu time = " + (endCpu - startCpu) / 1000 / 1000); // about 0ms
        System.out.println("time = " + (endTime - startTime)); // about 5000ms
    }

    public static void main(String[] args) throws Exception {
        threadMXBean();
    }
}
