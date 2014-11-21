
import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;

import javax.swing.Timer;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.ValueAxis;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.time.DynamicTimeSeriesCollection;
import org.jfree.data.time.Second;
import org.jfree.data.xy.XYDataset;
import org.jfree.ui.ApplicationFrame;
import org.jfree.ui.RefineryUtilities;

public class CPUMonitoringGraph extends ApplicationFrame {

    private static final String TITLE = "CPU Monitoring Graph";
    private static final int COUNT = 180;
    private static final int FAST = 100;
    private Timer timer;
    public static BufferedReader br;

    public CPUMonitoringGraph(final String title) {
        super(title);
        final DynamicTimeSeriesCollection dataset =
            new DynamicTimeSeriesCollection(1, COUNT, new Second());
        dataset.setTimeBase(new Second());
        dataset.addSeries(cpuData(), 0, "CPU data");
        JFreeChart chart = createChart(dataset);

        
        this.add(new ChartPanel(chart), BorderLayout.CENTER);
        timer = new Timer(FAST, new ActionListener() {
            float[] newData = new float[1];

            @Override
            public void actionPerformed(ActionEvent e) {
                newData[0] = fetchCPUData();
                dataset.advanceTime();
                dataset.appendData(newData);
            }
        });
    }

    private float fetchCPUData() {
    	String currentLine;
		try {
			if ((currentLine = br.readLine()) != null && !currentLine.trim().equals("")) {
					String[] currentValues = currentLine.split("\\|");
					float cpuValue = Float.valueOf(currentValues[1].trim());
					return cpuValue;
			}
		} catch (NumberFormatException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return (float) 0.0;
    }

    private float[] cpuData() {
        float[] a = new float[COUNT];
        for (int i = 0; i < a.length; i++) {
            a[i] = fetchCPUData();
        }
        return a;
    }

    private JFreeChart createChart(final XYDataset dataset) {
        final JFreeChart result = ChartFactory.createTimeSeriesChart(
            TITLE, "", "Value", dataset, true, true, false);
        final XYPlot plot = result.getXYPlot();
        ValueAxis domain = plot.getDomainAxis();
        domain.setAutoRange(true);
        ValueAxis range = plot.getRangeAxis();
        range.setRange(0, 3);
        return result;
    }

    public void start() {
        timer.start();
    }

    public static void main(final String[] args) throws FileNotFoundException {

    	if(args.length !=1)
    	{
    		System.out.println("Please provide valid inputs!");
    		return;
    	}
    	String vmid= args[0];
    	FileInputStream in = new FileInputStream("/var/lib/virtdc/logs/monitor_logs/"+vmid+".log");
		br = new BufferedReader(new InputStreamReader(in));
    	EventQueue.invokeLater(new Runnable() {

            @Override
            public void run() {
                CPUMonitoringGraph demo = new CPUMonitoringGraph(TITLE);
                demo.pack();
                RefineryUtilities.centerFrameOnScreen(demo);
                demo.setVisible(true);
                demo.start();
            }
        });
    }
}